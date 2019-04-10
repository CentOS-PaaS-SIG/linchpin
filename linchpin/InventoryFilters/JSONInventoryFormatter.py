#!/usr/bin/env python

import json

from .InventoryFormatter import InventoryFormatter


class JSONInventoryFormatter(InventoryFormatter):

    def __init__(self):
        InventoryFormatter.__init__(self)
        self.config = {}

    def add_sections(self, section_list):
        for section in section_list:
            self.config[section] = {}
        # adding a default section all
        if "all" not in self.config.keys():
            self.config["all"] = {}

    def set_children(self, inv):
        if 'host_groups' not in inv.keys():
            return
        for host_group in inv['host_groups']:
            if "children" in inv['host_groups'][host_group]:
                if not (host_group in self.config):
                    self.config[host_group] = {}
                self.config[host_group]["children"] = []
                for child in inv['host_groups'][host_group]['children']:
                    self.config[host_group]["children"].append(child)

    def set_vars(self, inv):
        if 'host_groups' not in inv.keys():
            return
        for host_group in inv['host_groups']:
            if "vars" in inv['host_groups'][host_group]:
                if not("vars" in self.config[host_group]):
                    self.config[host_group]["vars"] = {}
                host_grp_vars = inv['host_groups'][host_group]['vars']
                self.config[host_group]["vars"].update(host_grp_vars)
        for host in inv['hosts']:
            for host_group in host['host_groups']:
                self.config[host_group] = {}
        return True

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
                    self.config[host_group]["hosts"].append(ip)
                    if not (ip in self.config["all"]["hosts"]):
                        self.config["all"]["hosts"].append(ip)
        return True

    def add_ips_to_groups(self, inven_hosts, layout):
        ip_to_host = {}
        inven_hosts.reverse()
        self.add_ips_to_host_group("all", inven_hosts)
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
            for host_group in host_name['host_groups']:
                self.add_ips_to_host_group(host_group, host_list)
        return True


    def add_ips_to_host_group(self, host_group, hosts):
        for ip in hosts:
            if not ("hosts" in self.config[host_group]):
                self.config[host_group]['hosts'] = []
            self.config[host_group]["hosts"].append(ip)


    def add_common_vars(self, host_groups, layout, config):
        # defaults cvrs to [] when they doesnot exist
        # cvrs --> common_vars
        host_groups.append("all")
        cvrs = layout["vars"] if "vars" in layout.keys() else []
        for group in host_groups:
            items = self.config[group]["hosts"]
            if not("_meta" in self.config):
                self.config["_meta"] = {}
                self.config["_meta"]["hostvars"] = {}
            for item in items:
                for var in cvrs:
                    for cfg_item in config:
                        if item not in cfg_item.keys():
                            continue
                        if cvrs[var] in cfg_item[item].keys():
                            value = cvrs[var]
                            self.config["_meta"]["hostvars"][item] = \
                                cfg_item[item][value]
        return True

    def generate_inventory(self):
        return json.dumps(self.config)
