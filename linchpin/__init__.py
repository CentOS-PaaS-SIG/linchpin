#!/usr/bin/env python

import os
import re
import ast
import yaml
import json
import time
import hashlib

from collections import OrderedDict
from uuid import getnode as get_mac

from linchpin.ansible_runner import ansible_runner
from linchpin.utils import yaml2json
from linchpin.fetch import FETCH_CLASS

from linchpin.hooks.state import State
from linchpin.hooks import LinchpinHooks

from linchpin.rundb.basedb import BaseDB
from linchpin.rundb.drivers import DB_DRIVERS

from linchpin.exceptions import LinchpinError

class LinchpinAPI(object):

    def __init__(self, ctx):
        """
        LinchpinAPI constructor

        :param ctx: context object from context.py

        """

        self.ctx = ctx
        base_path = '/'.join(os.path.dirname(__file__).split('/')[0:-1])
        pkg = self.get_cfg(section='lp', key='pkg', default='linchpin')
        self.lp_path = '{0}/{1}'.format(base_path, pkg)

        self.set_evar('from_api', True)

        self.hook_state = None
        self._hook_observers = []
        self.playbook_pre_states = self.get_cfg('playbook_pre_states',
                                                {'up': 'preup',
                                                 'destroy': 'predestroy'})
        self.playbook_post_states = self.get_cfg('playbook_post_states',
                                                 {'up': 'postup',
                                                  'destroy': 'postdestroy',
                                                  'postinv': 'inventory'})
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

        return self.ctx.get_evar(key=key, default=default)


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


    def set_magic_vars(self, uhash):
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

        inv_folder = str(self.get_evar('inventories_folder'))

        inv_file = '{0}/{1}/{2}-{3}{4}'.format(self.workspace,
                                               inv_folder,
                                               topology_name,
                                               uhash,
                                               self.get_cfg('extensions',
                                                            'inventory',
                                                            'inventory'))

        self.set_evar('inventory_file', inv_file)
        self.set_evar('topology_name', topology_name)


    def lp_rise(self, pinfile, targets='all', run_id=None):
        """
        DEPRECATED

        An alias for lp_up. Used only for backward compatibility.
        """

        self.lp_up(pinfile, targets, run_id=run_id)


    def lp_up(self, pinfile, targets='all', run_id=None):
        """
        This function takes a list of targets, and provisions them according
        to their topology. If an layout argument is provided, an inventory
        will be generated for the provisioned nodes.

        :param pinfile:
            Provided PinFile, with available targets,

        :param targets:
            A tuple of targets to provision.
        """

        return self.run_playbook(pinfile, targets, action="up", run_id=run_id)


    def lp_drop(self, pinfile, targets, run_id=None):
        """
        DEPRECATED

        An alias for lp_destroy. Used only for backward compatibility.
        """

        return self.lp_destroy(pinfile, targets, run_id=run_id)


    def lp_destroy(self, pinfile, targets='all', run_id=None):
        """
        This function takes a list of targets, and performs a destructive
        teardown, including undefining nodes, according to the target.

        .. seealso:: lp_down - currently unimplemented

        :param pinfile:
            Provided PinFile, with available targets,

        :param targets:
            A tuple of targets to destroy.
        """

        return self.run_playbook(pinfile,
                                 targets,
                                 action="destroy",
                                 run_id=run_id)


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
            "topologies": self.get_evar("topologies_folder"),
            "layouts": self.get_evar("layouts_folder"),
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


    def lp_journal(self, targets=[], fields=None, count=None):

        rundb = self.setup_rundb()

        journal = {}

        if not len(targets):
            targets = rundb.get_tables()


        for target in targets:
            journal[target] = rundb.get_records(table=target, count=count)

        return journal


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


    def setup_rundb(self):
        """
        Configures the run database parameters, sets them into extra_vars
        """

        rundb_conn_default = '~/.config/linchpin/rundb-::mac::.json'
        rundb_conn = self.get_cfg(section='lp',
                                  key='rundb_conn',
                                  default=rundb_conn_default)
        rundb_type = self.get_cfg(section='lp',
                                  key='rundb_type',
                                  default='TinyRunDB')
        rundb_conn_type = self.get_cfg(section='lp',
                                       key='rundb_conn_type',
                                       default='file')
        self.rundb_hash = self.get_cfg(section='lp',
                                       key='rundb_hash',
                                       default='sha256')

        if rundb_conn_type == 'file':
            rundb_conn_int = rundb_conn.replace('::mac::', str(get_mac()))
            rundb_conn_int = os.path.expanduser(rundb_conn_int)
            rundb_conn_dir = os.path.dirname(rundb_conn_int)

            if not os.path.exists(rundb_conn_dir):
                os.mkdir(rundb_conn_dir)


        self.set_evar('rundb_type', rundb_type)
        self.set_evar('rundb_conn', rundb_conn_int)
        self.set_evar('rundb_hash', self.rundb_hash)


        return BaseDB(DB_DRIVERS[rundb_type], rundb_conn_int)


    def run_playbook(self, pinfile, targets=[], action='up', run_id=None):
        """
        This function takes a list of targets, and executes the given
        action (up, destroy, etc.) for each provided target.

        :param pinfile: Provided PinFile, with available targets,

        :param targets: A tuple of targets to run. (default: 'all')

        .. .note:: The `run_id` value differs from the `rundb_id`, in that
                   the `run_id` is an existing value in the database.
                   The `rundb_id` value is created to store the new record.
                   If the `run_id` is passed, it is used to collect an existing
                   `uhash` value from the given `run_id`, which is in turn used
                   to perform an idempotent reprovision, or destroy provisioned
                   resources.
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


        if action == 'destroy':
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

        # create localhost file in workspace for user if it doesn't exist
        if not os.path.exists('{0}/localhost'.format(self.workspace)):
            with open('{0}/localhost'.format(self.workspace), 'w') as f:
                f.write('localhost\n')

        for target in targets:

            results[target] = {}

            # initialize rundb table
            dateformat = self.get_cfg('logger',
                                      'dateformat',
                                      default='%m/%d/%Y %I:%M:%S %p')

            self.set_evar('target', target)

            rundb = self.setup_rundb()

            rundb_schema = json.loads(self.get_cfg(section='lp',
                                      key='rundb_schema'))
            rundb.schema = rundb_schema
            self.set_evar('rundb_schema', rundb_schema)

            start = time.strftime(dateformat)
            uhash = None

            # generate a new rundb_id
            # (don't confuse it with an already existing run_id)
            rundb_id = rundb.init_table(target)

            if action == 'up' and not run_id:
                uh = hashlib.new(self.rundb_hash,
                                 ':'.join([target, str(rundb_id), start]))
                uhash = uh.hexdigest()[-4:]
            elif action == 'destroy' or run_id:
                # look for the action='up' records to destroy
                data, orig_run_id = rundb.get_record(target,
                                                     action='up',
                                                     run_id=run_id)

                if data:
                    self.set_evar('orig_run_id', orig_run_id)
                    uhash = data.get('uhash')
                    self.ctx.log_debug("using data from"
                                       " run_id: {0}".format(run_id))
                else:
                    raise LinchpinError("Attempting to perform '{0}' action on"
                                        " target: '{1}' failed. No records"
                                        " available.".format(action, target))
            else:
                raise LinchpinError("run_id '{0}' does not match any existing"
                                    " records".format(run_id))


            self.ctx.log_debug('rundb_id: {0}'.format(rundb_id))
            self.ctx.log_debug('uhash: {0}'.format(uhash))
            rundb.update_record(target, rundb_id, 'uhash', uhash)

            rundb.update_record(target, rundb_id, 'start', start)
            rundb.update_record(target, rundb_id, 'action', action)

            self.set_evar('_action', action)
            self.set_evar('rundb_id', rundb_id)
            self.set_evar('uhash', uhash)

            self.set_evar('topology', self.find_topology(
                          pf[target]["topology"]))

            rundb.update_record(target,
                                rundb_id,
                                'inputs',
                                [
                                    {'topology_file': pf[target]['topology']}
                                ])

            if 'layout' in pf[target]:
                self.set_evar('layout_file',
                              '{0}/{1}/{2}'.format(self.ctx.workspace,
                                                   self.get_evar(
                                                       'layouts_folder'),
                                                   pf[target]["layout"]))

                ws = self.ctx.workspace
                layout_folder = self.get_evar("layouts_folder",
                                              default='layouts')
                layout_file = pf[target]['layout']
                layout_path = '{0}/{1}/{2}'.format(ws,
                                                   layout_folder,
                                                   layout_file)
                layout_data = yaml2json(layout_path)

                rundb.update_record(target,
                                    rundb_id,
                                    'inputs',
                                    [
                                        {'layout_file': layout_file}
                                    ])

                rundb.update_record(target,
                                    rundb_id,
                                    'inputs',
                                    [
                                        {'layout_data': layout_data}
                                    ])

            # parse topology_file and set inventory_file
            self.set_magic_vars(uhash)

            # set the current target data
            self.target_data = pf[target]
            self.target_data["extra_vars"] = self.get_evar()

            # note : changing the state triggers the hooks
            self.hooks.rundb = (rundb, rundb_id)
            self.pb_hooks = self.get_cfg('hookstates', action)
            self.ctx.log_debug('calling: {0}{1}'.format('pre', action))

            if 'pre' in self.pb_hooks:
                self.hook_state = '{0}{1}'.format('pre', action)

            # FIXME need to add rundb data for hooks results

            # invoke the appropriate action
            return_code, results[target]['task_results'] = (
                self._invoke_playbook(action=action,
                                      console=ansible_console)
            )

            if not return_code:
                self.ctx.log_state("Action '{0}' on Target '{1}' is "
                                   "complete".format(action, target))

            # FIXME Check the result[target] value here, and fail if applicable.
            # It's possible that a flag might allow more targets to run, then
            # return an error code at the end.

            # add post provision hook for inventory generation
            if 'inv' in self.pb_hooks:
                self.hook_state = 'postinv'

            if 'post' in self.pb_hooks:
                self.hook_state = '{0}{1}'.format('post', action)

            end = time.strftime(dateformat)
            rundb.update_record(target, rundb_id, 'end', end)
            rundb.update_record(target, rundb_id, 'rc', return_code)

            if action == 'destroy':
                run_data = rundb.get_record(target, action=action, run_id=orig_run_id)
            else:
                run_data = rundb.get_record(target, action=action, run_id=rundb_id)

            results[target]['rundb_data'] = {rundb_id: run_data[0]}

        return (return_code, results)


    def _invoke_playbook(self, action='up', console=True):
        """
        Uses the Ansible API code to invoke the specified linchpin playbook

        :param action: Which ansible action to run (default: 'up')
        :param console: Whether to display the ansible console (default: True)
        """

        pb_path = '{0}/{1}'.format(self.lp_path,
                                   self.ctx.get_evar('playbooks_folder',
                                                     'provision'))
        module_path = '{0}/{1}/'.format(pb_path, self.get_cfg('lp',
                                                              'module_folder',
                                                              'library'))
        playbook_path = '{0}/{1}'.format(pb_path, self.get_cfg('playbooks',
                                                               action,
                                                               'site.yml'))
        extra_var = self.get_evar()

        return ansible_runner(playbook_path,
                              module_path,
                              extra_var,
                              console=console)
