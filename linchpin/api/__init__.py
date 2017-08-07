#!/usr/bin/env python

import os
import re
import sys
import ast
import yaml
from collections import namedtuple, OrderedDict
from contextlib import contextmanager

from ansible.inventory import Inventory
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor

from linchpin.api.utils import yaml2json
from linchpin.api.callbacks import PlaybookCallback
from linchpin.api.fetch import FETCH_CLASS
from linchpin.hooks import LinchpinHooks
from linchpin.hooks.state import State
from linchpin.exceptions import LinchpinError


@contextmanager
def suppress_stdout():
    """
    This context manager provides tooling to make Ansible's Display class
    not output anything when used
    """

    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull

        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


class LinchpinAPI(object):

    def __init__(self, ctx):
        """
        LinchpinAPI constructor

        :param ctx: context object from api/context.py

        """

        self.ctx = ctx
        base_path = '/'.join(os.path.dirname(__file__).split('/')[0:-2])
        pkg = self.get_cfg(section='lp',
                           key='pkg',
                           default='linchpin')
        self.lp_path = '{0}/{1}'.format(base_path, pkg)
        self.set_evar('from_api', True)

        self.hook_state = None
        self._hook_observers = []
        self.playbook_pre_states = self.get_cfg('playbook_pre_states',
                                                {'up': 'preup',
                                                 'destroy': 'predestroy'})
        self.playbook_post_states = self.get_cfg('playbook_post_states',
                                                 {'up': 'postup',
                                                  'destroy': 'postdestroy'})
        self.hooks = LinchpinHooks(self)
        self.target_data = {}

        if not self.workspace:
            self.workspace = os.path.realpath(os.path.curdir)


    def get_cfg(self, section=None, key=None, default=None):
        """
        Get cfgs value(s) by section and/or key, or the whole cfgs object

        :param section: section from ini-style config file

        :param key: key to get from config file, within section

        :param default: default value to return if nothing is found.

        Does not apply if section is not provided.
        """

        return self.ctx.get_cfg(section=section, key=key, default=default)


    def set_cfg(self, section, key, value):
        """
        Set a value in cfgs. Does not persist into a file,
        only during the current execution.


        :param section: section within ini-style config file

        :param key: key to use

        :param value: value to set into section within config file
        """

        self.ctx.set_cfg(section, key, value)


    def get_evar(self, key=None, default=None):
        """
        Get the current evars (extra_vars)

        :param key: key to use

        :param default: default value to return if nothing is found
        (default: None)
        """

        return self.ctx.get_evar(key, default)


    def set_evar(self, key, value):
        """
        Set a value into evars (extra_vars). Does not persist into a file,
        only during the current execution.

        :param key: key to use

        :param value: value to set into evars
        """

        self.ctx.set_evar(key, value)


    @property
    def pinfile(self):
        """
        getter function for pinfile name
        """

        return self.ctx.pinfile


    @pinfile.setter
    def pinfile(self, pinfile):
        """
        setter for pinfile name
        """

        self.ctx.pinfile = pinfile


    @property
    def workspace(self):
        """
        getter function for context workspace
        """

        return self.ctx.workspace


    @workspace.setter
    def workspace(self, workspace):
        """
        setter for context workspace
        """

        self.ctx.workspace = workspace


    @property
    def hook_state(self):
        """
        getter function for hook_state property of the API object
        """

        return self.hook_state


    @hook_state.setter
    def hook_state(self, hook_state):
        """
        hook_state property setter , splits the hook_state string in
        subhook_state and sets linchpin.hook_state object

        :param hook_state: valid hook_state string mentioned in linchpin.conf
        """

        # call run_hooks after hook_state is being set
        if hook_state is None:
            return
        else:
            self.ctx.log_debug('hook {0} initiated'.format(hook_state))
            self._hook_state = State(hook_state, None, self.ctx)

            for callback in self._hook_observers:
                callback(self._hook_state)


    def bind_to_hook_state(self, callback):
        """
        Function used by LinchpinHooksclass to add callbacks

        :param callback: callback function
        """

        self._hook_observers.append(callback)


    def set_magic_vars(self):
        """
        Function inbuilt to set magic vars for ansible context
        """

        try:
            t_f = open(self.get_evar("topology"), "r").read()
            t_f = yaml.load(t_f)
            topology_name = t_f["topology_name"]
        except Exception as e:
            self.ctx.log_info("{0}".format(str(e)))
            topology_name = self.get_evar("topology").split("/")[-1]
            # defaults to file name if there is any error
            topology_name = topology_name.split(".")[-2]

        inv_file = '{0}/{1}/{2}{3}'.format(self.workspace,
                                           self.get_evar('inventories_folder'),
                                           topology_name,
                                           self.get_cfg('extensions',
                                                        'inventory',
                                                        'inventory'))

        self.set_evar('inventory_file', inv_file)
        self.set_evar('topology_name', topology_name)

    def run_playbook(self, pinfile, targets='all', playbook='up'):
        """
        This function takes a list of targets, and executes the given
        playbook (provison, destroy, etc.) for each provided target.

        :param pinfile: Provided PinFile, with available targets,

        :param targets: A tuple of targets to run. (default: 'all')
        """

        pf = yaml2json(pinfile)

        # playbooks check whether from_api is defined
        self.ctx.log_debug('from_api: {0}'.format(self.get_evar('from_api')))

        # playbooks check whether from_cli is defined
        # if not, vars get loaded from linchpin.conf
        self.set_evar('from_api', True)
        self.set_evar('lp_path', self.lp_path)

        # do we display the ansible output to the console?
        ansible_console = False
        if self.ctx.cfgs.get('ansible'):
            ansible_console = (
                ast.literal_eval(self.ctx.cfgs['ansible'].get('console',
                                                              'False')))

        if not ansible_console:
            ansible_console = self.ctx.verbose

        self.set_evar('default_resources_path', '{0}/{1}'.format(
                      self.ctx.workspace,
                      self.get_evar('resources_folder',
                                    default='resources')))

        # playbooks still use this var, keep it here
        self.set_evar('default_inventories_path',
                      '{0}/{1}'.format(self.ctx.workspace,
                                       self.get_evar('inventories_folder',
                                                     default='inventories')))

        # add this because of magic_var evaluation in ansible
        self.set_evar('inventory_dir', self.get_evar(
                      'default_inventories_path',
                      default='inventories'))

        self.set_evar('state', 'present')


        if playbook == 'destroy':
            self.set_evar('state', 'absent')

        results = {}

        # determine what targets is equal to
        if (set(targets) ==
                set(pf.keys()).intersection(targets) and len(targets) > 0):
            pass
        elif len(targets) == 0:
            targets = set(pf.keys()).difference()
        else:
            raise LinchpinError("One or more invalid targets found")


        for target in targets:
            self.set_evar('topology', self.find_topology(
                          pf[target]["topology"]))

            if 'layout' in pf[target]:
                self.set_evar('layout_file',
                              '{0}/{1}/{2}'.format(self.ctx.workspace,
                                                   self.get_evar(
                                                       'layouts_folder'),
                                                   pf[target]["layout"]))

            # parse topology_file and set inventory_file
            self.set_magic_vars()

            # set the current target data
            self.target_data = pf[target]
            self.target_data["extra_vars"] = self.get_evar()

            # note : changing the state triggers the hooks
            self.pb_hooks = self.get_cfg('hookstates', playbook)
            self.ctx.log_debug('calling: {0}{1}'.format('pre', playbook))

            if 'pre' in self.pb_hooks:
                self.hook_state = '{0}{1}'.format('pre', playbook)

            # invoke the appropriate playbook
            return_code, results[target] = (
                self._invoke_playbook(playbook=playbook,
                                      console=ansible_console)
            )

            if not return_code:
                self.ctx.log_state("Action '{0}' on Target '{1}' is "
                                   "complete".format(playbook, target))

            # FIXME Check the result[target] value here, and fail if applicable.
            # It's possible that a flag might allow more targets to run, then
            # return an error code at the end.

            if 'post' in self.pb_hooks:
                self.hook_state = '{0}{1}'.format('post', playbook)

        return results


    def lp_rise(self, pinfile, targets='all'):
        """
        DEPRECATED

        An alias for lp_up. Used only for backward compatibility.
        """

        self.lp_up(pinfile, targets)


    def lp_up(self, pinfile, targets='all'):
        """
        This function takes a list of targets, and provisions them according
        to their topology. If an layout argument is provided, an inventory
        will be generated for the provisioned nodes.

        :param pinfile:
            Provided PinFile, with available targets,

        :param targets:
            A tuple of targets to provision.
        """

        return self.run_playbook(pinfile, targets, playbook="up")


    def lp_drop(self, pinfile, targets):
        """
        DEPRECATED

        An alias for lp_destroy. Used only for backward compatibility.
        """

        return self.lp_destroy(pinfile, targets)


    def lp_destroy(self, pinfile, targets='all'):
        """
        This function takes a list of targets, and performs a destructive
        teardown, including undefining nodes, according to the target.

        .. seealso:: lp_down - currently unimplemented

        :param pinfile:
            Provided PinFile, with available targets,

        :param targets:
            A tuple of targets to destroy.
        """

        return self.run_playbook(pinfile, targets, playbook="destroy")


    def lp_down(self, pinfile, targets='all'):
        """
        This function takes a list of targets, and performs a shutdown on
        nodes in the target's topology. Only providers which support shutdown
        from their API (Ansible) will support this option.

        CURRENTLY UNIMPLEMENTED

        .. seealso:: lp_destroy

        :param pinfile:
            Provided PinFile, with available targets,

        :param targets:
            A tuple of targets to provision.
        """

        pass


    def lp_fetch(self, src, fetch_type, root):
        if root is not None:
            root = list(filter(None, root.split(',')))

        dest = self.ctx.workspace
        if not os.path.exists(dest):
            raise LinchpinError(dest + " does not exist")

        fetch_aliases = {
            "topology": self.get_evar("topologies_folder"),
            "layout": self.get_evar("layouts_folder"),
            "resources": self.get_evar("resources_folder"),
            "hooks": self.get_evar("hooks_folder"),
            "workspace": "workspace"
        }

        fetch_dir = fetch_aliases.get(fetch_type, "workspace")


        cache_path = os.path.abspath(os.path.join(os.path.expanduser('~'),
                                                  '.cache/linchpin'))
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)

        protocol_regex = OrderedDict([
            ('((git|ssh|http(s)?)|(git@[\w\.]+))'
                '(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?',
                'FetchGit'),
            ('^(http|https)://', 'FetchHttp'),
            ('^(file)://', 'FetchLocal')
        ])
        fetch_protocol = None
        for regex, obj in protocol_regex.items():
            if re.match(regex, src):
                fetch_protocol = obj
                break
        if fetch_protocol is None:
            raise LinchpinError("The protocol speficied is not supported")


        fetch_class = FETCH_CLASS[fetch_protocol](self.ctx, fetch_dir, src,
                                                  dest, cache_path, root)
        fetch_class.fetch_files()

        fetch_class.copy_files()


    def find_topology(self, topology):
        """
        Find the topology to be acted upon. This could be pulled from a
        registry.

        :param topology:
            name of topology from PinFile to be loaded

        """

        topo_path = os.path.realpath('{0}/{1}'.format(
                                     self.ctx.workspace,
                                     self.get_evar('topologies_folder',
                                                   'topologies')))

        topos = os.listdir(topo_path)

        if topology in topos:
            return os.path.realpath('{0}/{1}'.format(topo_path, topology))

        raise LinchpinError('Topology {0} not found in'
                            ' workspace'.format(topology))



    def _invoke_playbook(self, playbook='up', console=True):
        """
        Uses the Ansible API code to invoke the specified linchpin playbook

        :param playbook: Which ansible playbook to run (default: 'up')
        :param console: Whether to display the ansible console (default: True)
        """

        pb_path = '{0}/{1}'.format(self.lp_path,
                                   self.ctx.get_evar('playbooks_folder',
                                                     'provision'))
        module_path = '{0}/{1}/'.format(pb_path, self.get_cfg('lp',
                                                              'module_folder',
                                                              'library'))
        playbook_path = '{0}/{1}'.format(pb_path, self.get_cfg('playbooks',
                                                               playbook,
                                                               'site.yml'))

        loader = DataLoader()
        variable_manager = VariableManager()
        variable_manager.extra_vars = self.get_evar()
        inventory = Inventory(loader=loader,
                              variable_manager=variable_manager,
                              host_list=[])
        passwords = {}
        # utils.VERBOSITY = 4

        Options = namedtuple('Options', ['listtags',
                                         'listtasks',
                                         'listhosts',
                                         'syntax',
                                         'connection',
                                         'module_path',
                                         'forks',
                                         'remote_user',
                                         'private_key_file',
                                         'ssh_common_args',
                                         'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args',
                                         'become',
                                         'become_method',
                                         'become_user',
                                         'verbosity',
                                         'check'])

        options = Options(listtags=False,
                          listtasks=False,
                          listhosts=False,
                          syntax=False,
                          connection='ssh',
                          module_path=module_path,
                          forks=100,
                          remote_user='test',
                          private_key_file=None,
                          ssh_common_args=None,
                          ssh_extra_args=None,
                          sftp_extra_args=None,
                          scp_extra_args=None,
                          become=False,
                          become_method='sudo',
                          become_user='root',
                          verbosity=0,
                          check=False)

        pbex = PlaybookExecutor(playbooks=[playbook_path],
                                inventory=inventory,
                                variable_manager=variable_manager,
                                loader=loader,
                                options=options,
                                passwords=passwords)

        if not console:
            results = {}
            return_code = 0

            cb = PlaybookCallback()

            with suppress_stdout():
                pbex._tqm._stdout_callback = cb

            return_code = pbex.run()
            results = cb.results

            return return_code, results
        else:
            # the console only returns a return_code
            return_code = pbex.run()
            return return_code, None
