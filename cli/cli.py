import os
from linchpin_api.v1.api import LinchpinAPI
from linchpin_api.v1.invoke_playbooks import invoke_linchpin
from utils import parse_yaml


class LinchpinCli(LinchpinAPI):

    def __init__(self):
        LinchpinAPI.__init__(self)

    def test(self):
        print("test function inside linchpincli")

    def lp_topo_list(self, upstream=None):
        return LinchpinAPI.lp_topo_list(self, upstream)

    def lp_layout_list(self, upstream=None):
        return LinchpinAPI.lp_layout_list(self, upstream)

    def find_topology(self, topology, pf):
        config = self.get_config()
        print("Finding topology in local folder ./topology")
        topos = os.listdir("./topologies")
        if topology in topos:
            return os.path.abspath("./topologies/"+topology)
        print("Not found")
        print("Finding topology in package ")
        topos = self.lp_topo_list()
        topos = [x["name"] for x in topos]
        if topology in topos:
            print("Found!! copying it to local folder")
            self.lp_topo_get(topology)
            return os.path.abspath("./topologies/"+topology)
        print("Not found")
        print("Finding topology from upstream")
        topos = self.lp_topo_list(pf["topology_upstream"])
        topos = [x["name"] for x in topos]
        if topology in topos:
            print("Found!!")
            print("Fetching topology from upstream !")
            self.lp_topo_get(topology, pf["topology_upstream"])
            return os.path.abspath("./topologies/"+topology)
        print("Not Found !!")
        return None

    def find_layout(self, layout, pf):
        config = self.get_config()
        try:
            print("Finding layout in local folder ./layouts")
            layouts = os.listdir("./layouts")
            if layout in layouts:
                return os.path.abspath("./layouts/"+layout)
            print("Not found")
            print("Finding layout in package ")
            layouts = self.lp_layout_list()
            layouts = [x["name"] for x in layouts]
            if layout in layouts:
                print("Found!! copying it to local folder")
                self.lp_layout_get(layout)
                return os.path.abspath("./layouts/"+layout)
            print("Not found")
            print("Finding layout from upstream")
            layouts = self.lp_layout_list(pf["layout_upstream"])
            layouts = [x["name"] for x in layouts]
            if layout in layouts:
                print("Found!!")
                print("Fetching layout from upstream !")
                self.lp_topo_get(layout, pf["layout_upstream"])
                return os.path.abspath("./layouts/"+topology)
            print("Not Found !!")
        except Exception as e:
            print(e)

    def lp_rise(self, pf, target):
        pf = parse_yaml(pf)
        init_dir = os.getcwd()
        e_vars = {}
        e_vars['linchpin_config'] = self.get_config_path()
        e_vars['outputfolder_path'] = init_dir+"/outputs"
        e_vars['inventory_outputs_path'] = init_dir+"/inventories"
        e_vars['state'] = "present"
        if target == "all":
            for key in set(pf.keys()).difference(self.excludes):
                e_vars['topology'] = self.find_topology(pf[key]["topology"],
                                                        pf)
                if e_vars['topology'] is None:
                    print("Topology not found !!")
                    break
                if pf[key].has_key('layout'):
                    layout_path = self.find_layout(pf[key]["layout"], pf)
                    e_vars['inventory_layout_file'] = layout_path
                    if e_vars['inventory_layout_file'] is None:
                        print("Layout not found !!")
                        break
                    print(e_vars)
                output = invoke_linchpin(self.base_path,
                                         e_vars,
                                         "PROVISION",
                                         console=True)
        else:
            if pf.get(target, False):
                topology_path = self.find_topology(pf[target]["topology"],
                                                   pf)
                e_vars['topology'] = topology_path
                if e_vars['topology'] is None:
                    print("Topology not found !!")
                if pf[key].has_key('layout'):
                    layout_path = self.find_layout(pf[target]["layout"], pf)
                    e_vars['inventory_layout_file'] = layout_path
                    if e_vars['inventory_layout_file'] is None:
                        print("Layout not found !!")
                    print(e_vars)
                output = invoke_linchpin(self.base_path,
                                         e_vars,
                                         "PROVISION",
                                         console=True)
            else:
                raise KeyError('Target not found in PinFile')

    def lp_drop(self, pf, target):
        """ drop module of linchpin cli :
        still need to fix the linchpin_config and outputs,
        inventory_outputs paths"""
        pf = parse_yaml(pf)
        init_dir = os.getcwd()
        e_vars = {}
        e_vars['linchpin_config'] = self.get_config_path()
        e_vars['inventory_outputs_path'] = init_dir + "/inventories"
        e_vars['state'] = "absent"
        if target == "all":
            for key in set(pf.keys()).difference(self.excludes):
                e_vars['topology'] = self.find_topology(pf[key]["topology"],
                                                        pf)
                topo_name = pf[key]["topology"].strip(".yml").strip(".yaml")
                output_path = init_dir + "/outputs/" + topo_name + ".output"
                e_vars['topology_output_file'] = output_path
                output = invoke_linchpin(self.base_path,
                                         e_vars,
                                         "TEARDOWN",
                                         console=True)
        else:
            print(pf[target])
            if pf.get(target, False):
                topology_path = self.find_topology(pf[target]["topology"],
                                                   pf)
                e_vars['topology'] = topology_path
                if e_vars['topology'] is None:
                    print("Topology not found !!")
                topo_name = pf[target]["topology"]
                topo_name = topo_name.strip(".yml").strip(".yaml")
                output_path = init_dir + "/outputs/" + topo_name + ".output"
                e_vars['topology_output_file'] = output_path
                output = invoke_linchpin(self.base_path,
                                         e_vars,
                                         "TEARDOWN",
                                         console=True)
