#!/usr/bin/env python
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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

        if 'results' in res.keys():
            for result in res.get('results', []):
                if 'openstack' in result.keys():
                    os_vars = result.get('openstack', [])
                    host = self.get_hostname(os_vars, var_data,
                                             self.DEFAULT_HOSTNAMES)
                    hostname_var = host[0]
                    hostname = host[1]
                    host_data[hostname] = {}
                    if '__IP__' not in var_data.keys():
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
                    if '__IP__' not in var_data.keys():
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
                if '__IP__' not in var_data.keys():
                    var_data['__IP__'] = hostname_var
                    host_data[hostname] = {}
                host_data[hostname] = {}
                self.set_config_values(host_data[hostname], grp, var_data)
        return host_data


    def get_host_ips(self, host_data):
        return host_data.keys()

    def get_inventory(self, topo, layout, config):
        host_data = []
        inven_hosts = []
        for res in topo:
            hd = self.get_host_data(res, config)
            if hd:
                host_data.append(hd)
            inven_hosts = self.get_host_ips(hd)
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
