#!/usr/bin/env python

import json
import StringIO

from InventoryFilter import InventoryFilter
from InventoryFormatter import InventoryFormatter

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

class JSONInventoryFormatter(InventoryFormatter):

    def __init__(self):
        InventoryFormatter.__init__(self)
        self.config = {}

    def add_sections(self, section_list):
        for section in section_list:
            #self.config.add_section(section)
            self.config[section] = {}
        # adding a default section all
        if "all" not in self.config.keys():
            self.config["all"] = {}

    def set_children(self, inv):
        if 'host_groups' not in inv.keys():
            return
        for host_group in inv['host_groups']:
            if "children" in inv['host_groups'][host_group]:
                #self.config.add_section("{0}:children".format(host_group))
                if not (host_group in self.config):
                    self.config[host_group] = {}
                self.config[host_group]["children"] = []
                for child in inv['host_groups'][host_group]['children']:
                    #self.config.set("{0}:children".format(host_group), child)
                    self.config[host_group]["children"].append(child)

    def set_vars(self, inv):
        if 'host_groups' not in inv.keys():
            return
        for host_group in inv['host_groups']:
            if "vars" in inv['host_groups'][host_group]:
                #self.config.add_section("{0}:vars".format(host_group))
                if not( "vars" in self.config[host_group]):
                    self.config[host_group]["vars"] = {}
                self.config[host_group]["vars"].update(inv['host_groups'][host_group]['vars'])
        return True
                #for var in inv['host_groups'][host_group]['vars']:
                #    grp_vars = inv['host_groups'][host_group]['vars'][var]
                #    grp_vars = str(grp_vars)
                #    self.config.set(host_group + ":" + "vars", var, grp_vars)

    def add_ips_to_groups(self, inven_hosts, layout):
        # create a ip to host mapping based on count
        ip_to_host = {}
        inven_hosts.reverse()
        for host_name in layout['hosts']:
            if 'count' in host_name.keys():
                count = host_name['count']
            else:
                count = 1
            host_list = []
            if count > len(inven_hosts):
                count = len(inven_hosts)
            for i in range(count, 0, -1):
                item = inven_hosts.pop()
                host_list.append(item)
            ip_to_host[host_name["name"]] = host_list
        # add ips to the respective host groups in inventory
        for host_name in layout['hosts']:
            host_ips = ip_to_host[host_name["name"]]
            for ip in host_ips:
                for host_group in host_name['host_groups']:
                    if not ("hosts" in self.config[host_group]):
                        self.config[host_group]["hosts"] = []
                    if not ("hosts" in self.config["all"]):
                        self.config["all"]["hosts"] = []
                    #self.config.set(host_group, ip)
                    self.config[host_group]["hosts"].append(ip)
                    if not (ip in self.config["all"]["hosts"]):
                        self.config["all"]["hosts"].append(ip)
                    #self.config.set("all", ip)
        return True

    def add_common_vars(self, host_groups, layout):
        # defaults common_vars to [] when they doesnot exist
        host_groups.append("all")
        common_vars = layout["vars"] if "vars" in layout.keys() else []
        for group in host_groups:
            #items = dict(self.config.items(group)).keys()
            items = self.config[group]["hosts"]
            #self.config.remove_section(group)
            #self.config.add_section(group)
            if not("_meta" in self.config):
                self.config["_meta"] = {}
                self.config["_meta"]["hostvars"] = {}
            for item in items:
                #self.config["_meta"]["hostvars"][item] = {}
                host_string = item
                for var in common_vars:
                    self.config["_meta"]["hostvars"][item]= {}
                    if common_vars[var] == "__IP__":
                        self.config["_meta"]["hostvars"][item][var] = item 
                        #host_string += " " + var + "=" + item
                    else:
                        #host_string += " " + var + "=" + common_vars[var]
                        #host_string += " " + var + "=" + common_vars[var]
                        self.config["_meta"]["hostvars"][item][var] = common_vars[var] 

#            for item in items:
#                host_string = item
#                for var in common_vars:
#                    if common_vars[var] == "__IP__":
#                        host_string += " " + var + "=" + item
#                    else:
#                        host_string += " " + var + "=" + common_vars[var]
#                self.config.set(group, host_string)
        return True

    def generate_inventory(self):
        return json.dumps(self.config)
