#!/usr/bin/env python

from __future__ import absolute_import
from collections import OrderedDict
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from linchpin.InventoryFilters.InventoryFilter import InventoryFilter


class Inventory(InventoryFilter):
    DEFAULT_HOSTNAMES = ['ipv4', 'ipv6']

    def get_host_data(self, res, cfgs):
        """
        Returns a dict of hostnames or IP addresses for use in an Ansible
        inventory file, based on available data. Only a single hostname or IP
        address will be returned per instance, so as to avoid duplicate runs of
        Ansible on the same host via the generated inventory file.

        Each hostname contains mappings of any variable that was defined in the
        cfgs section of the PinFile (e.g. __IP__) to the value in the field that
        corresponds with that variable in the cfgs.

         :param topo:
            linchpin VMware guest resource data

        :param cfgs:
            map of config options from PinFile
        """

        host_data = OrderedDict()
        if res['resource_group'] != 'vmware' or res['role'] != 'vmware_guest':
            return host_data
        var_data = cfgs.get('vmware', {})
        if var_data is None:
            var_data = {}
        instance = res['instance']
        host = self.get_hostname(instance, var_data, self.DEFAULT_HOSTNAMES)
        hostname_var = host[0]
        hostname = host[1]
        if '__IP__' not in var_data.keys():
            var_data['__IP__'] = hostname_var
        host_data[hostname] = {}
        self.set_config_values(host_data[hostname], instance, var_data)
        return host_data

    def get_host_ips(self, host_data):
        if host_data:
            return host_data.keys()
        else:
            return []

    def get_inventory(self, topo, layout, config):
        host_data = []
        inven_hosts = []
        for res in topo:
            hd = self.get_host_data(res, config)
            if hd:
                host_data.append(hd)
            inven_hosts.extend(self.get_host_ips(hd))
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
        output = StringIO()
        self.config.write(output)
        return output.getvalue()
