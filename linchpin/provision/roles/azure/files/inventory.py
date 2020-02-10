from __future__ import absolute_import
from collections import OrderedDict

from linchpin.InventoryFilters.InventoryFilter import InventoryFilter


class Inventory(InventoryFilter):
    # DEFAULT_HOSTNAMES = ['public_dns_name', 'public_ip', 'private_ip']

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
            linchpin Azure VM resource data

        :param cfgs:
            map of config options from PinFile
        """

        host_data = OrderedDict()
        if res['resource_group'] != 'azure'or res['role'] != 'azure_vm':
            return host_data
        var_data = cfgs.get('azure', {})
        if var_data is None:
            var_data = {}
        networks = res['properties']['networkProfile']['networkInterfaces']
        for network in networks:
            mid = network['properties']['ipConfigurations'][0]
            # mid: this is a middle variable for flake test
            ip = mid['properties']['publicIPAddress']['properties']['ipAddress']
            host_data[ip] = {"__IP__": ip}
            self.set_config_values(host_data[ip], res, var_data)
        return host_data
