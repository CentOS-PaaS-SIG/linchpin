#!/usr/bin/env python

import os
import ast
from collections import namedtuple

from ansible.inventory import Inventory
from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor

from linchpin.api.invoke_playbooks import invoke_linchpin
from linchpin.api.utils import yaml2json
from linchpin.api.callbacks import PlaybookCallback
from linchpin.hooks import LinchpinHooks
from linchpin.hooks.state import State


class LinchpinError(Exception):

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)


class LinchpinAPI(object):

    def __init__(self, ctx):

        self.ctx = ctx
        base_path = '/'.join(os.path.dirname(__file__).split("/")[0:-2])
        self.lp_path = '{0}/{1}'.format(base_path, self.ctx.cfgs['lp']['pkg'])
        ctx.evars['from_api'] = True


    def get_cfg(self, section=None, key=None):
        """
        Get the cfgs object

        :param section: section from ini-style config file

        :param key: key to get from config file, within section
        """
        if section:
            s = self.ctx.cfgs.get(section, None)
            if key and s:
                return self.ctx.cfgs[section].get(key, None)
            return s
        return self.ctx.cfgs

    def set_cfg(self, section, key, value):
        """
        Set a value in cfgs. Does not persist into a file,
        only during the current execution.


        :param section: section within ini-style config file

        :param key: key to use

        :param value: value to set into section within config file
        """

        self.ctx.cfgs[section][key] = value


    def get_evar(self, key=None):
        """
        Get the current evars (extra_vars)

        :param key: key to use
        """

        if key:
            return self.ctx.evars.get(key, None)
        return self.evars

        self._state = None
        self._state_observers = []
        self.hooks = LinchpinHooks(self)
        self.current_target_data = {}

    @property
    def state(self):
        """ getter function for state property of the API object. """
        return self._state

    @state.setter
    def state(self, state):
        # call run_hooks after state is being set
        self.ctx.log_debug("State change initiated")
        value = state.split("::")
        state = value[0]
        sub_state = value[-1] if len(value) > 1 else None
        self._state = State(state,
                            sub_state
                            )
        for callback in self._state_observers:
            callback(self._state)

    def bind_to_state(self, callback):
        self._state_observers.append(callback)

    def set_evar(self, key, value):
        """
        Set a value into evars (extra_vars). Does not persist into a file,
        only during the current execution.

        :param key: key to use

        :param value: value to set into evars
        """

        self.set_cfg('evars', key, value)
        self.evars[key] = value


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
        self.ctx.evars['from_cli'] = True
        self.ctx.evars['lp_path'] = self.lp_path

        self.console = ast.literal_eval(self.ctx.cfgs['ansible'].get('console', 'False'))

        if not self.console:
            self.console = self.ctx.verbose

        self.ctx.evars['default_resources_path'] = '{0}/{1}'.format(
                                self.ctx.workspace,
                                self.ctx.evars['resources_folder'])
        self.ctx.evars['default_inventories_path'] = '{0}/{1}'.format(
                                self.ctx.workspace,
                                self.ctx.evars['inventories_folder'])
        self.ctx.evars['state'] = "present"
        if playbook == 'destroy':
            self.ctx.evars['state'] = "absent"

        results = {}

        # checks whether the targets are valid or not
        if set(targets) == set(pf.keys()).intersection(targets) and len(targets) > 0:
            for target in targets:
                self.ctx.log_state('target: {0}, action: {1}'.format(target, playbook))
                self.ctx.evars['topology'] = self.find_topology(
                        pf[target]["topology"])
                if 'layout' in pf[target]:
                    self.ctx.evars['layout_file'] = (
                        '{0}/{1}/{2}'.format(self.ctx.workspace,
                                    self.ctx.evars['layouts_folder'],
                                    pf[target]["layout"]))
                self.current_target_data = pf[target]
                self.current_target_data["extra_vars"] = self.ctx.evars
                # set the state to preup/predown based on playbook
                # note : changing the state triggers the hooks
                if playbook == "provision":
                    self.state = "preup"
                elif playbook == "destroy":
                    self.state = "predown"

                #invoke the appropriate playbook
                results[target] = self._invoke_playbook(playbook=playbook,
                                                console=self.console)
                # note : changing the state triggers the hooks
                if playbook == "provision":
                    self.prepare_ctx_params()
                    self.state = "postup"
                elif playbook == "destroy":
                    self.prepare_ctx_params()
                    self.state = "postdown"

            return results

        elif len(targets) == 0:
            for target in set(pf.keys()).difference():
                self.ctx.log_state('target: {0}, action: {1}'.format(target, playbook))
                self.ctx.evars['topology'] = self.find_topology(
                        pf[target]["topology"])
                if 'layout' in pf[target]:
                    self.ctx.evars['layout_file'] = (
                        '{0}/{1}/{2}'.format(self.ctx.workspace,
                                    self.ctx.evars['layouts_folder'],
                                    pf[target]["layout"]))
                self.current_target_data = pf[target]
                self.current_target_data["extra_vars"] = self.ctx.evars
                
                # set the state to preup/predown based on playbook
                # note : changing the state triggers the hooks
                if playbook == "provision":
                    self.state = "preup"
                elif playbook == "destroy":
                    self.state = "predown"

                #invoke the appropriate playbook
                results[target] = self._invoke_playbook(playbook=playbook,
                                                console=self.console)
                if playbook == "provision":
                    self.prepare_ctx_params()
                    self.state = "postup"
                elif playbook == "destroy":
                    self.prepare_ctx_params()
                    self.state = "postdown"
            return results

        else:
            raise  KeyError("One or more Invalid targets found")


    def lp_rise(self, pinfile, targets='all'):
                # set the current target data
                self.current_target_data = pf[target]
                self.current_target_data["extra_vars"] = self.ctx.evars
                # set the state to preup/predown based on playbook
                # note : changing the state triggers the hooks
                if playbook == "provision":
                    self.state = "preup"
                elif playbook == "destroy":
                    self.state = "predown"
                #invoke the PROVISION linch-pin playbook
                output = invoke_linchpin(
                                            self.ctx,
                                            self.lp_path,
                                            self.ctx.evars,
                                            playbook=playbook
                                        )
                # set the state to postup/postdown based on playbook
                # note : changing the state triggers the hooks
                if playbook == "provision":
                    self.prepare_ctx_params()
                    self.state = "postup"
                elif playbook == "destroy":
                    self.prepare_ctx_params()
                    self.state = "postdown"
        else:
            raise  KeyError("One or more Invalid targets found")

    def lp_rise(self, pf, targets='all'):

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

        topo_path = os.path.realpath('{}/{}'.format(
                self.ctx.workspace,
                self.ctx.evars['topologies_folder']))

        topos = os.listdir(topo_path)

        if topology in topos:
            return os.path.realpath('{0}/{1}'.format(topo_path, topology))

        return None


    def _invoke_playbook(self, playbook='up', console=True):

        """
        Uses the Ansible API code to invoke the specified linchpin playbook

        :param playbook: Which ansible playbook to run (default: 'up')
        :param console: Whether to display the ansible console (default: True)
        """

        pb_path = '{0}/{1}'.format(self.lp_path, self.ctx.evars['playbooks_folder'])
        module_path = '{0}/{1}'.format(pb_path, self.ctx.cfgs['lp']['module_folder'])
        playbook_path = '{0}/{1}'.format(pb_path, self.ctx.cfgs['playbooks'][playbook])

        loader = DataLoader()
        variable_manager = VariableManager()
        variable_manager.extra_vars = self.ctx.evars
        inventory = Inventory(loader=loader,
                              variable_manager=variable_manager,
                              host_list=[])
        passwords = {}
        utils.VERBOSITY = 4

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
                          verbosity=utils.VERBOSITY,
                          check=False)

        pbex = PlaybookExecutor(playbooks=[playbook_path],
                                inventory=inventory,
                                variable_manager=variable_manager,
                                loader=loader,
                                options=options,
                                passwords=passwords)

        if not console:
            cb = PlaybookCallback()
            pbex._tqm._stdout_callback = cb
            return_code = pbex.run()
            results = cb.results
        else:
            results = pbex.run()

        return results


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
