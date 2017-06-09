#!/usr/bin/env python

import os
import sys
import ast
import yaml
from collections import namedtuple
from contextlib import contextmanager

from ansible.inventory import Inventory
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor


from linchpin.api.utils import yaml2json
from linchpin.api.callbacks import PlaybookCallback
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

        :param default: default value to return if nothing is found (default: None)
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
    def hook_state(self):
        """
        getter function for hook_state property of the API object
        """

        return self.hook_state


    @hook_state.setter
    def hook_state(self, hook_state):
        """
        hook_state property setter , splits the hook_state string in subhook_state and sets
        linchpin.hook_state object

        :param hook_state: valid hook_state string mentioned in linchpin.conf
        """

        # call run_hooks after hook_state is being set
        if hook_state is None:
            return
        else:
#            hook_state = hook_state.split('::')[0]
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
        inv_file = '{0}/{1}/{2}{3}'.format(self.ctx.workspace,
                        self.get_evar('inventories_folder'),
                        topology_name,
                        self.get_cfg('extensions','inventory' ,'inventory')
                    )
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

        #do we display the ansible output to the console?
        ansible_console = False
        if self.ctx.cfgs.get('ansible'):
            ansible_console = ast.literal_eval(self.ctx.cfgs['ansible'].get('console', 'False'))

        if not ansible_console:
            ansible_console = self.ctx.verbose

        self.set_evar('default_resources_path', '{0}/{1}'.format(
                                            self.ctx.workspace,
                                            self.get_evar('resources_folder',
                                                    default='resources')))

        # playbooks still use this var, keep it here
        self.set_evar('default_inventories_path', '{0}/{1}'.format(
                                        self.ctx.workspace,
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
        if (set(targets) == set(pf.keys()).intersection(targets) and
                                                        len(targets) > 0):
            pass
        elif len(targets) == 0:
            targets = set(pf.keys()).difference()
        else:
            raise LinchpinError("One or more Invalid targets found")


        for target in targets:
            self.set_evar('topology', self.find_topology(
                    pf[target]["topology"]))

            if 'layout' in pf[target]:
                self.set_evar('layout_file', (
                    '{0}/{1}/{2}'.format(self.ctx.workspace,
                                self.get_evar('layouts_folder'),
                                pf[target]["layout"])))

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

            #invoke the appropriate playbook
            return_code, results[target] = self._invoke_playbook(
                                            playbook=playbook,
                                            console=ansible_console)

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


    def find_topology(self, topology):
        """
        Find the topology to be acted upon. This could be pulled from a
        registry.

        :param topology:
            name of topology from PinFile to be loaded

        """

        topo_path = os.path.realpath('{0}/{1}'.format(
                self.ctx.workspace,
                self.get_evar('topologies_folder', 'topologies')))

        topos = os.listdir(topo_path)

        if topology in topos:
            return os.path.realpath('{0}/{1}'.format(topo_path, topology))

        raise LinchpinError('Topology {0} not found in workspace'.format(topology))



    def _invoke_playbook(self, playbook='up', console=True):
        """
        Uses the Ansible API code to invoke the specified linchpin playbook

        :param playbook: Which ansible playbook to run (default: 'up')
        :param console: Whether to display the ansible console (default: True)
        """

        pb_path = '{0}/{1}'.format(self.lp_path,
                            self.ctx.get_evar('playbooks_folder', 'provision'))
        module_path = '{0}/{1}/'.format(pb_path, self.get_cfg('lp', 'module_folder', 'library'))
        playbook_path = '{0}/{1}'.format(pb_path, self.get_cfg('playbooks', playbook, 'site.yml'))

        loader = DataLoader()
        variable_manager = VariableManager()
        variable_manager.extra_vars = self.get_evar()
        inventory = Inventory(loader=loader,
                              variable_manager=variable_manager,
                              host_list=[])
        passwords = {}
        #utils.VERBOSITY = 4

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


#    def lp_topo_list(self, upstream=None):
#        """
#        search_order : list topologies from upstream if mentioned
#                       list topologies from current folder
#        """
#        if upstream is None:
#            t_files = list_files(self.base_path + "/examples/topology/")
#            return t_files
#        else:
#            print("getting from upstream")
#            g = GitHub(upstream)
#            t_files = []
#            repo_path = LinchpinAPI.UPSTREAM_EXAMPLES_PATH + "/topology"
#            files = g.list_files(repo_path)
#            return files
#
#    REPLACED ABOVE (but it doesn't do the registry lookup yet)
#    def find_topology(self, topology, topolgy_registry):
#        print("searching for topology in configured workspace: "+self.context.workspace)
#        try:
#            topos = os.listdir(self.context.workspace+"/topologies")
#            if topology in topos:
#                return os.path.abspath(self.context.workspace+"/topologies/"+topology)
#        except OSError as e:
#            click.echo(str(e))
#            click.echo("topologies directory  not found in workspace.")
#        except Exception as e:
#            click.echo(str(e))
#        click.echo("Searching for topology in linchpin package.")
#        topos = self.lp_topo_list()
#        topos = [t["name"] for t in topos]
#        if topology in topos:
#            click.echo("Topology file found in linchpin package.")
#            click.echo("Copying it to workspace")
#            self.lp_topo_get(topology)
#            return os.path.abspath(self.context.workspace+"/topologies/"+topology)
#        click.echo("Topology file not found")
#        click.echo("Searching for topology from upstream")
#        # currently supports only one topology registry per PinFile
#        if topology_registry:
#            try:
#                topos = self.lp_topo_list(topology_registry)
#                topos = [x["name"] for x in topos]
#                if topology in topos:
#                    click.echo("Found topology in registry")
#                    click.echo("Fetching topology from registry")
#                    self.lp_topo_get(topology, topology_registry)
#                    return os.path.abspath(self.context.workspace+"/topologies/"+topology)
#            except Exception as e:
#                click.echo("Exception occurred "+str(e))
#        raise IOError("Topology file not found. Invalid topology reference in PinFile")
#
#    def find_layout(self, layout, layout_registry=None):
#        print("searching for layout in configured workspace: "+self.context.workspace)
#        try:
#            layouts = os.listdir(self.context.workspace+"/layouts")
#            if layout in layouts:
#                return os.path.abspath(self.context.workspace+"/layouts/"+layout)
#        except OSError as e:
#            click.echo(str(e))
#            click.echo("layouts directory  not found in workspace.")
#        except Exception as e:
#            click.echo(str(e))
#        click.echo("Searching for layout in linchpin package.")
#        layouts = self.lp_layout_list()
#        layouts = [t["name"] for t in layouts]
#        if layout in layouts:
#            click.echo("layout file found in linchpin package.")
#            click.echo("Copying it to workspace")
#            self.lp_layout_get(layout)
#            return os.path.abspath(self.context.workspace+"/layouts/"+layout)
#        click.echo("layout file not found")
#        click.echo("Searching for layout from upstream")
#        # currently supports only one layout registry per PinFile
#        if layout_registry:
#            try:
#                layouts = self.lp_layout_list(layout_registry)
#                layouts = [x["name"] for x in layouts]
#                if layout in layouts:
#                    click.echo("Found layout in registry")
#                    click.echo("Fetching layout from registry")
#                    self.lp_layout_get(layout, layout_registry)
#                    return os.path.abspath(self.context.workspace+"/layouts/"+layout)
#            except Exception as e:
#                click.echo("Exception occurred "+str(e))
#        raise IOError("layout file not found. Invalid layout reference in PinFile")
#
#    def lp_topo_get(self, topo, upstream=None):
#        """
#        search_order : get topologies from upstream if mentioned
#                       get topologies from core package
#        # need to add checks for ./topologies
#        """
#        if upstream is None:
#            pkg_file_path = self.base_path + "/examples/topology/" + topo
#            return open(pkg_file_path).read()
#            #get_file(self.base_path + "/examples/topology/" + topo,
#            #         "./topologies/")
#        else:
#            g = GitHub(upstream)
#            repo_path = LinchpinAPI.UPSTREAM_EXAMPLES_PATH + "/topology"
#            files = g.list_files(repo_path)
#            link = filter(lambda link: link['name'] == topo, files)
#            link = link[0]["download_url"]
#            return requests.get(link).text
#            #get_file(link, "./topologies", True)
#            #return link
#
#    def lp_layout_list(self, upstream=None):
#        """
#        search_order : list layouts from upstream if mentioned
#                       list layouts from core package
#        """
#        if upstream is None:
#            l_files = list_files(self.base_path + "examples/layouts/")
#            return l_files
#        else:
#            g = GitHub(upstream)
#            l_files = []
#            repo_path = LinchpinAPI.UPSTREAM_EXAMPLES_PATH + "/layouts"
#            files = g.list_files(repo_path)
#            return files
#
#    def lp_layout_get(self, layout, upstream=None):
#        """
#        search_order : get layouts from upstream if mentioned
#                       get layouts from core package
#        """
#        if upstream is None:
#            pkg_file_path = self.base_path + "/examples/layouts/" + layout
#            return open(pkg_file_path, "r").read()
#            #get_file(self.base_path + "/examples/layouts/" + layout,
#            #         "./layouts/")
#        else:
#            g = GitHub(upstream)
#            repo_path = LinchpinAPI.UPSTREAM_EXAMPLES_PATH + "/layouts"
#            files = g.list_files(repo_path)
#            link = filter(lambda link: link['name'] == layout, files)
#            link = link[0]["download_url"]
#            return requests.get(link).text
#
#
#
#    def lp_validate_topology(self, topology):
#        self.evars = {}
#        self.evars["schema"] = self.base_path + "/schemas/schema_v3.json"
#        self.evars["data"] = topology
#        result = invoke_linchpin(self.base_path, self.evars,
#                                 "SCHEMA_CHECK", console=True)
#        print(result)
#        return result
#
#
#    def lp_invgen(self, topoout, layout, invout, invtype):
#        """ invgen module of linchpin cli """
#        self.evars = {}
#        self.evars['linchpin_config'] = self.get_config_path()
#        self.evars['output'] = os.path.abspath(topoout)
#        self.evars['layout'] = os.path.abspath(layout)
#        self.evars['inventory_type'] = invtype
#        self.evars['inventory_output'] = invout
#        result = invoke_linchpin(self.base_path,
#                                 self.evars,
#                                 "INVGEN",
#                                 console=True)
#
#    def lp_test(self, topo, layout, pf):
#        """ test module of linchpin.api"""
#        self.evars = {}
#        self.evars['data'] = topo
#        self.evars['schema'] = self.base_path + "/schemas/schema_v3.json"
#        result = invoke_linchpin(self.base_path, self.evars, "TEST", console=True)
#        return result
