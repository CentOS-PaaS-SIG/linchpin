#!/usr/bin/env python
import abc
import json
import StringIO
from ansible import errors

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from InventoryFilter import InventoryFilter


class OpenstackInventory(InventoryFilter):

    def get_host_ips(self, topo):
        host_public_ips = []
        for group in topo['os_server_res']:
            grp = group.get('openstack', [])
            if isinstance(grp, list):
                for server in grp:
                    host_public_ips.append(str(server['accessIPv4']))
            if isinstance(grp, dict):
                host_public_ips.append(str(grp['accessIPv4']))
        return host_public_ips

    def get_inventory(self, topo, layout):

        if len(topo['os_server_res']) == 0:
            return ""
        no_of_groups = len(topo['os_server_res'])
        inven_hosts = self.get_host_ips(topo)
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
