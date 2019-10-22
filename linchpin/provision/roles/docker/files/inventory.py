from __future__ import absolute_import
from collections import OrderedDict

from linchpin.InventoryFilters.InventoryFilter import InventoryFilter


class Inventory(InventoryFilter):
    DEFAULT_HOSTNAMES = ['Config.Hostname']

    def get_host_data(self, res, config):
        # Only docker_container resource type produces host data.
        if res['resource_group'] != 'docker':
            return {}

        if res['role'] == 'docker_container':
            return self.get_docker_container_host_data(res, config)
        else:
            return {}

    def get_docker_container_host_data(self, res, config):
        host_data = OrderedDict()

        var_data = config.get('docker', {})
        if var_data is None:
            var_data = {}
        host = self.get_hostname(res, var_data,
                                 self.DEFAULT_HOSTNAMES)
        hostname_var = host[0]
        hostname = host[1]
        host_data[hostname] = {}
        if '__IP__' not in var_data.keys():
            var_data['__IP__'] = hostname_var
        self.set_config_values(host_data[hostname], res, var_data)
        return host_data
