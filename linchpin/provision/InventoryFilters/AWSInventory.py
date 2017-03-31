#!/usr/bin/env python

import abc
import StringIO
from ansible import errors

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from InventoryFilter import InventoryFilter


class AWSInventory(InventoryFilter):

    def get_host_ips(self, topo):

        host_public_ips = []
        for group in topo['aws_ec2_res']:
            for instance in group['instances']:
                host_public_ips.append(str(instance['public_dns_name']))
        return host_public_ips

    def get_inventory(self, topo, layout):

        if len(topo['aws_ec2_res']) == 0:
            return ""
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
