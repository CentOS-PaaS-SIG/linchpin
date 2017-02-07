#!/usr/bin/env python

import abc
import StringIO
from ansible import errors

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from InventoryFilter import InventoryFilter


class DuffyInventory(InventoryFilter):

    def get_hostnames(self, topo):
        hostnames = []
        for group in topo['duffy_res']:
            for host in group['hosts']:
                hostnames.append(host)
        return hostnames

    def get_host_ips(self, topo):
        return self.get_hostnames(topo)

    def add_hosts_to_groups(self, config, inven_hosts, layout):
        # create a ip to host mapping based on count
        hosts = {}
        for host_name in layout['hosts']:
            count = layout['hosts'][host_name]['count']
            host_list = []
            hosts[host_name] = [host_list.append(inven_hosts.pop())
                                for inven_hosts in range(count)]
            for ip in host_ips:
                for host_group in layout['hosts'][host_name]['host_groups']:
                    config.set(host_group, ip)
        return config

    def get_inventory(self, topo, layout):
        if len(topo['duffy_res']) == 0:
            return ""
        inventory = ConfigParser(allow_no_value=True)
        layout_hosts = self.get_layout_hosts(layout)
        inven_hosts = self.get_hostnames(topo)
        # adding sections to respective host groups
        host_groups = self.get_layout_host_groups(layout)
        self.add_sections(host_groups)
        # set children for each host group
        self.set_children(layout)
        # set vars for each host group
        self.set_vars(layout)
        # add ip addresses to each host
        self.add_ips_to_groups(inven_hosts, layout)
        self.add_common_vars(host_groups, layout)
        output = StringIO.StringIO()
        self.config.write(output)
        return output.getvalue()
