import os
import inspect
import ansible
import pprint
import linchpin_api
from tabulate import tabulate
from ansible import utils
import jsonschema as jsch
from collections import namedtuple
from ansible import utils
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from callbacks import PlaybookCallback
from invoke_playbooks import invoke_linchpin
from utils import get_file, list_files, parse_yaml
from github import GitHub


class LinchpinAPI:

    def __init__(self):
        self.PLAYBOOKS = {
                           "PROVISION": "site.yml",
                           "TEARDOWN": "site.yml",
                           "SCHEMA_CHECK": "schema_check.yml",
                           "INVGEN": "invgen.yml",
                         }
        base_path = os.path.dirname(__file__).split("/")
        base_path = base_path[0:-2]
        self.base_path = "/".join(base_path)
        self.excludes = set(["topology_upstream",
                             "layout_upstream",
                             "post_actions"])

    def get_config_path(self):
        try:
            cwd = os.getcwd()
            config_files = [
                            cwd+"/linchpin_config.yml",
                            "~/.linchpin_config.yml",
                            self.base_path+"/linchpin_config.yml",
                            "/etc/linchpin_config.yml"]
            for c_file in config_files:
                if os.path.isfile(c_file):
                    return c_file
        except Exception as e:
            print(e)

    def get_config(self):
        config_path = self.get_config_path()
        config = parse_yaml(config_path)
        return config

    def get_evars(self, lpf):
        """ creates a group of extra vars on basis on linchpin file dict """
        e_vars = []
        for group in lpf:
            topology = lpf[group].get("topology")
            layout = lpf[group].get("layout")
            e_var_grp = {}
            e_var_grp["topology"] = search_path(topology, os.getcwd())
            e_var_grp["layout"] = search_path(layout, os.getcwd())
            if None in e_var_grp.values():
                display("ERROR:003")
            e_vars.append(e_var_grp)
        return e_vars

    def lp_list(self, config, topos=False, layouts=False):
        """ list module of linchpin  """
        if topos and layouts:
            t_files = list_files(config.clipath+"/ex_topo")
            l_files = list_files(config.clipath+"/inventory_layouts")
            return (t_files, l_files)
        if topos:
            t_files = list_files(config.clipath+"/ex_topo")
            return t_files
        if layouts:
            l_files = list_files(config.clipath+"/inventory_layouts")
            return l_files

    def lp_topo_list(self, upstream=None):
        """
        search_order : list topologies from upstream if mentioned
                       list topologies from current folder
        """
        if upstream is None:
            t_files = list_files(self.base_path + "/ex_topo")
            return t_files
        else:
            print "getting from upstream"
            g = GitHub(upstream)
            t_files = []
            files = g.list_files("ex_topo")
            return files

    def lp_topo_get(self, topo, upstream=None):
        """
        search_order : get topologies from upstream if mentioned
                       get topologies from core package
        # need to add checks for ./topologies
        """
        if upstream is None:
            get_file(self.base_path + "/ex_topo/" + topo, "./topologies/")
        else:
            g = GitHub(upstream)
            files = g.list_files("ex_topo")
            link = filter(lambda link: link['name'] == topo, files)
            link = link[0]["download_url"]
            get_file(link, "./topologies", True)
            return link

    def lp_layout_list(self, upstream=None):
        """
        search_order : list layouts from upstream if mentioned
                       list layouts from core package
        """
        if upstream is None:
            l_files = list_files(self.base_path + "/inventory_layouts")
            return l_files
        else:
            g = GitHub(upstream)
            l_files = []
            files = g.list_files("inventory_layouts")
            return files

    def lp_layout_get(self, layout, upstream=None):
        """
        search_order : get layouts from upstream if mentioned
                       get layouts from core package
        """
        if upstream is None:
            get_file(self.base_path + "/inventory_layouts/" + layout,
                     "./layouts/")
        else:
            g = GitHub(upstream)
            files = g.list_files("inventory_layouts")
            link = filter(lambda link: link['name'] == layout, files)
            link = link[0]["download_url"]
            get_file(link, "./layouts", True)
            return link

    def lp_drop(self, config, lpf):
        """ drop module of linchpin cli : find implementation in cli.py
        inventory_outputs paths"""
        """
        config.variable_manager.extra_vars = {}
        init_dir = os.getcwd()
        lpfs = list_by_ext(init_dir, ".lpf")
        if len(lpfs) == 0:
            display("ERROR:001")
        if len(lpfs) > 1:
            display("ERROR:002")
        lpf = lpfs[0]
        lpf = parse_yaml(lpf)
        e_vars_grp = get_evars(lpf)
        for e_vars in e_vars_grp:
            e_vars['linchpin_config'] = "/etc/linchpin/linchpin_config.yml"
            topo_name = parse_yaml(e_vars["topology"])["topology_name"]
            e_vars['topology_output_file'] = init_dir + "/outputs/" + \
                                                        topo_name + ".output"
            e_vars['inventory_outputs_path'] = init_dir + "/inventory"
            e_vars['state'] = "absent"
            invoke_linchpin(config, e_vars, "PROVISION", console=True)
        """

    def lp_rise(self, lpf, target):
        """ rise module of linchpin cli find implementation in cli.py"""
        """
        init_dir = os.getcwd()
        lpfs = list_by_ext(init_dir, "PinFile")
        lpf = lpfs[0]
        lpf = parse_yaml(lpf)
        e_vars_grp = get_evars(lpf)
        for e_vars in e_vars_grp:
            e_vars['linchpin_config'] = self.get_config_path()
            e_vars['outputfolder_path'] = init_dir+"/outputs"
            e_vars['inventory_outputs_path'] = init_dir+"/inventory"
            e_vars['state'] = "present"
            output = invoke_linchpin(config, e_vars, "PROVISION", console=True)
        """

    def lp_validate(self, topo, layout, lpf):
        """ validate module of linchpin cli :
        currenly validates only topologies,
        need to implement lpf, layouts too"""
        e_vars = {}
        e_vars["schema"] = self.base_path + "/ex_schemas/schema_v3.json"
        e_vars["data"] = topo
        result = invoke_linchpin(self.base_path, e_vars,
                                 "SCHEMA_CHECK", console=False)
        return result[0].__dict__

    def lp_invgen(self, topoout, layout, invout, invtype):
        """ invgen module of linchpin cli """
        e_vars = {}
        e_vars['linchpin_config'] = self.get_config_path()
        e_vars['output'] = os.path.abspath(topoout)
        e_vars['layout'] = os.path.abspath(layout)
        e_vars['inventory_type'] = invtype
        e_vars['inventory_output'] = invout
        result = invoke_linchpin(self.base_path,
                                 e_vars,
                                 "INVGEN",
                                 console=True)

    def lp_test(self, topo, layout, lpf):
        """ test module of linchpin_api"""
        e_vars = {}
        e_vars['data'] = topo
        e_vars['schema'] = self.base_path + "/ex_schemas/schema_v3.json"
        result = invoke_linchpin(self.base_path, e_vars, "TEST", console=True)
        return result
