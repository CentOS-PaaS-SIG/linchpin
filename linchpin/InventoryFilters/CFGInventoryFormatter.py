#!/usr/bin/env python

try:
    from StrinIO import StringIO
except ImportError:
    from io import StringIO

import collections

from .InventoryFormatter import InventoryFormatter

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


class CFGInventoryFormatter(InventoryFormatter):

    def __init__(self):
        InventoryFormatter.__init__(self)
        self.config = ConfigParser(allow_no_value=True)

    def add_sections(self, section_list):
        for section in section_list:
            self.config.add_section(section)
        # adding a default section all
        if "all" not in self.config.sections():
            self.config.add_section("all")

    def set_children(self, inv):
        if 'host_groups' not in inv.keys():
            return
        for host_group in inv['host_groups']:
            if "children" in inv['host_groups'][host_group]:
                self.config.add_section("{0}:children".format(host_group))
                for child in inv['host_groups'][host_group]['children']:
                    self.config.set("{0}:children".format(host_group), child)

    def set_vars(self, inv):
        if 'host_groups' not in inv.keys():
            return
        for host_group in inv['host_groups']:
            if "vars" in inv['host_groups'][host_group]:
                self.config.add_section("{0}:vars".format(host_group))
                for var in inv['host_groups'][host_group]['vars']:
                    grp_vars = inv['host_groups'][host_group]['vars'][var]
                    grp_vars = str(grp_vars)
                    self.config.set(host_group + ":" + "vars", var, grp_vars)


    def add_ips_to_groups(self, inven_hosts, layout):
        # create a ip to host mapping based on count
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
            for host_group in host_name['host_groups']:
                self.add_ips_to_host_group(host_group, host_list)
        return True


    def add_ips_to_host_group(self, host_group, hosts):
        for ip in hosts:
            self.config.set(host_group, ip)


    def add_common_vars(self, host_groups, layout, config):
        # defaults common_vars to [] when they doesnot exist
        host_groups.append("all")
        common_vars = layout['vars'] if 'vars' in layout.keys() else []
        for group in host_groups:
            items = collections.OrderedDict(self.config.items(group)).keys()
            self.config.remove_section(group)
            self.config.add_section(group)
            for item in items:
                host_string = item
                for var in common_vars:
                    for cfg_item in config:
                        if item not in cfg_item.keys():
                            continue
                        if common_vars[var] in cfg_item[item].keys():
                            value = common_vars[var]
                            host_string += " " + var + "=" +\
                                           str(cfg_item[item][value])
                        else:
                            host_string += " " + var + "=" +\
                                           str(common_vars[var])
                self.config.set(group, host_string)

    def generate_inventory(self):
        output = StringIO()
        self.config.write(output)
        return output.getvalue()
