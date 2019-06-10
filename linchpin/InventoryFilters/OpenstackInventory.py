#!/usr/bin/env python
from __future__ import absolute_import

from .InventoryFilter import InventoryFilter


class OpenstackInventory(InventoryFilter):
    DEFAULT_HOSTNAMES = ["accessIPv4", "public_v4", "private_v4"]

    def get_host_data(self, res, cfgs):
        host_data = {}
        if res['resource_type'] != 'os_server_res':
            return host_data
        var_data = cfgs.get('openstack', {})
        if var_data is None:
            var_data = {}

        if 'results' in list(res.keys()):
            for result in res.get('results', []):
                if 'openstack' in list(result.keys()):
                    os_vars = result.get('openstack', [])
                    host = self.get_hostname(os_vars, var_data,
                                             self.DEFAULT_HOSTNAMES)
                    hostname_var = host[0]
                    hostname = host[1]
                    host_data[hostname] = {}
                    if '__IP__' not in list(var_data.keys()):
                        var_data['__IP__'] = hostname_var
                        host_data[hostname] = {}
                    self.set_config_values(host_data[hostname], os_vars,
                                           var_data)
                else:
                    continue
        else:
            grp = res.get('openstack', [])
            if isinstance(grp, list):
                for server in grp:
                    host = self.get_hostname(server, var_data,
                                             self.DEFAULT_HOSTNAMES)
                    hostname_var = host[0]
                    hostname = host[1]
                    host_data[hostname] = {}
                    if '__IP__' not in list(var_data.keys()):
                        var_data['__IP__'] = hostname_var
                        host_data[hostname] = {}
                    host_data[hostname] = {}
                    self.set_config_values(host_data[hostname], server,
                                           var_data)
            if isinstance(grp, dict):
                host = self.get_hostname(grp, var_data,
                                         self.DEFAULT_HOSTNAMES)
                hostname_var = host[0]
                hostname = host[1]
                host_data[hostname] = {}
                if '__IP__' not in list(var_data.keys()):
                    var_data['__IP__'] = hostname_var
                    host_data[hostname] = {}
                host_data[hostname] = {}
                self.set_config_values(host_data[hostname], grp, var_data)
        return host_data
