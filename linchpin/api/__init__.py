#!/usr/bin/env python

import os

from linchpin.api.invoke_playbooks import invoke_linchpin
from linchpin.api.utils import yaml2json


class LinchpinError(Exception):

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class LinchpinAPI:

    def __init__(self, ctx):

        self.ctx = ctx
        base_path = '/'.join(os.path.dirname(__file__).split("/")[0:-2])
        self.lp_path = '{0}/{1}'.format(base_path, self.ctx.cfgs['lp']['pkg'])

        self._load_global_evars()


    def _load_global_evars(self):

        """
        Instantiate the evars variable, then load the variables from the
        'evars' section in linchpin.conf. This will then be passed to
        invoke_linchpin, which passes them to the Ansible playbook as needed.

        """

        self.evars = self.ctx.cfgs.get('evars', None)

    def run_playbook(self, pinfile, targets='all', playbook='provision'):


        """
        This function takes a list of targets, and executes the given
        playbook (provison, destroy, etc.) for each provided target.

        \b
        pf:
            Provided PinFile, with available targets,

        \b
        targets:
            A tuple of targets to run.
        """

        pf = yaml2json(pinfile)

        # playbooks check whether from_cli is defined
        # if not, vars get loaded from linchpin.conf
        self.evars['from_cli'] = True
        self.evars['lp_path'] = self.lp_path

        self.evars['default_resources_path'] = '{0}/{1}'.format(
                                self.ctx.workspace,
                                self.ctx.cfgs['lp']['resources_folder'])
        self.evars['default_inventories_path'] = '{0}/{1}'.format(
                                self.ctx.workspace,
                                self.ctx.cfgs['lp']['inventories_folder'])

        self.evars['state'] = "present"

        if playbook == 'destroy':
            self.evars['state'] = "absent"


        # checks wether the targets are valid or not
        if set(targets) == set(pf.keys()).intersection(targets) and len(targets) > 0:
            for target in targets:
                self.ctx.log_state('Provisioning target: {0}'.format(target))
                topology = pf[target]['topology']
                topology_registry = pf.get("topology_registry", None)
                self.evars['topology'] = find_topology(pf[target]["topology"],
                                                        topology_registry)
                if pf[target].has_key("layout"):
                    self.evars['layout_file'] = (
                        '{0}/{1}/{2}'.format(self.ctx.workspace,
                                    self.ctx.cfgs['lp']['layouts_folder'],
                                    pf[target]["layout"]))


#                def invoke_linchpin(ctx, lp_path, self.evars, playbook='provision', console=True):
                #invoke the PROVISION linch-pin playbook
                output = invoke_linchpin(
                                            self.ctx,
                                            self.lp_path,
                                            self.evars,
                                            playbook=playbook
                                        )

        elif len(targets) == 0:
            for target in set(pf.keys()).difference():
                self.ctx.log_state('Provisioning target: {0}'.format(target))
                topology = pf[target]['topology']
                topology_registry = pf.get("topology_registry", None)
                self.evars['topology'] = self.find_topology(pf[target]["topology"],
                                                        topology_registry)
                if pf[target].has_key("layout"):
                    self.evars['layout_file'] = (
                        '{0}/{1}/{2}'.format(self.ctx.workspace,
                                    self.ctx.cfgs['lp']['layouts_folder'],
                                    pf[target]["layout"]))



                #invoke the PROVISION linch-pin playbook
                output = invoke_linchpin(
                                            self.ctx,
                                            self.lp_path,
                                            self.evars,
                                            playbook=playbook
                                         )

        else:
            raise  KeyError("One or more Invalid targets found")


    def lp_rise(self, pf, targets='all'):

        """
        DEPRECATED

        An alias for lp_up. Used only for backward compatibility.
        """

        self.lp_up(pf, targets)


    def lp_up(self, pinfile, targets='all'):


        """
        This function takes a list of targets, and provisions them according
        to their topology. If an layout argument is provided, an inventory
        will be generated for the provisioned nodes.

        \b
        pf:
            Provided PinFile, with available targets,

        \b
        targets:
            A tuple of targets to provision.
        """

        self.run_playbook(pinfile, targets, playbook="provision")


    def lp_drop(self, pf, targets):

        """
        DEPRECATED

        An alias for lp_destroy. Used only for backward compatibility.
        """

        self.lp_destroy(pf, targets)


    def lp_destroy(self, pf, targets):


        """
        This function takes a list of targets, and performs a destructive
        teardown, including undefining nodes, according to the target.

        \b
        SEE ALSO:
            lp_down - currently unimplemented

        \b
        pf:
            Provided PinFile, with available targets,

        \b
        targets:
            A tuple of targets to destroy.
        """

        self.run_playbook(pf, targets, playbook="destroy")


    def lp_down(self, pf, targets):


        """
        This function takes a list of targets, and performs a shutdown on
        nodes in the target's topology. Only providers which support shutdown
        from their API (Ansible) will support this option.

        \b
        CURRENTLY UNIMPLEMENTED

        \b
        SEE ALSO:
            lp_destroy

        \b
        pf:
            Provided PinFile, with available targets,

        \b
        targets:
            A tuple of targets to provision.
        """

        pass



    def find_topology(self, topology, topo_reg):


        """
        Find the topology to be acted upon. This could be pulled from a
        registry.

        \b
        topology:
            name of topology from PinFile to be loaded

        \b
        topo_reg:
            registry (optional) where the topology may be found.

            Default:
                $WORKSPACE/layouts/LAYOUT_NAME
        """

        topo_path = os.path.realpath('{}/{}'.format(
                self.ctx.workspace,
                self.ctx.cfgs['lp']['topologies_folder']))

        topos = os.listdir(topo_path)

        if topology in topos:
            return os.path.realpath('{0}/{1}'.format(topo_path, topology))

        return None


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
