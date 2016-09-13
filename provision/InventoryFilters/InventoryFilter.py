#!/usr/bin/env python
import abc
import StringIO
from ansible import errors
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


class InventoryFilter(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_host_ips(self, topo, layout):
        pass

    def get_layout_hosts(self, inv):
        count = 0
        for host_group in inv['hosts']:
            count += inv['hosts'][host_group]['count']
        return count

    def get_layout_host_groups(self, inv):
        return inv['host_groups'].keys()

    def add_sections(self, config, section_list):
        for section in section_list:
            config.add_section(section)
        return config

    def set_children(self, config, inv):
        for host_group in inv['host_groups']:
            if "children" in inv['host_groups'][host_group]:
                config.add_section(host_group+":"+"children")
                for child in inv['host_groups'][host_group]['children']:
                    config.set(host_group+":"+"children", child)
        return config

    def set_vars(self, config, inv):
        for host_group in inv['host_groups']:
            if "vars" in inv['host_groups'][host_group]:
                config.add_section(host_group+":"+"vars")
                for var in inv['host_groups'][host_group]['vars']:
                    config.set(host_group+":"+"vars", var, inv['host_groups'][host_group]['vars'][var])
        return config

    def add_ips_to_groups(self, config, inven_hosts, layout):
        # create a ip to host mapping based on count
        ip_to_host = {}
        for host_name in layout['hosts']:
            count = layout['hosts'][host_name]['count']
            host_list = []
            for i in range(0, count):
                item = inven_hosts.pop()
                host_list.append(item)
            ip_to_host[host_name] = host_list
        # add ips to the host groups in inventory 
        for host_name in layout['hosts']:
            host_ips = ip_to_host[host_name]
            for ip in host_ips:
                for host_group in layout['hosts'][host_name]['host_groups']:
                    config.set(host_group, ip)
        return config

    def add_common_vars(self, config, host_groups, layout):
        common_vars = layout['vars']
        for group in host_groups:
            items = dict(config.items(group)).keys()
            config.remove_section(group)
            config.add_section(group)
            for item in items:
                host_string = item
                for var in common_vars:
                    if common_vars[var] == "__IP__":
                        host_string += " " + var + "=" + item + " "
                config.set(group, host_string)
        return config

    @abc.abstractmethod
    def get_inventory(self, topo, layout):
        pass
