#!/usr/bin/env python
import StringIO

from InventoryFilter import InventoryFilter


class OpenstackInventory(InventoryFilter):
    DEFAULT_HOSTNAMES = ["accessIPv4", "public_v4", "private_v4"]

    def get_host_data(self, topo, cfgs):
        host_data = {}
        var_data = cfgs.get('openstack', {})
        if var_data is None:
            var_data = {}

        for group in topo['os_server_res']:
            if 'results' in group.keys():
                for res in group.get('results', []):
                    if 'openstack' in res.keys():
                        os_vars = res.get('openstack', [])
                        hostname = self.get_hostname(os_vars, var_data,
                                                     self.DEFAULT_HOSTNAMES)
                        host_data[hostname] = {}
                        self.set_config_values(host_data[hostname], os_vars,
                                               var_data)
                    else:
                        continue
            else:
                grp = group.get('openstack', [])
                if isinstance(grp, list):
                    for server in grp:
                        hostname = self.get_hostname(server, var_data,
                                                     self.DEFAULT_HOSTNAMES)
                        host_data[hostname] = {}
                        self.set_config_values(host_data[hostname], server,
                                               var_data)
                if isinstance(grp, dict):
                    hostname = self.get_hostname(grp, var_data,
                                                 self.DEFAULT_HOSTNAMES)
                    host_data[hostname] = {}
                    self.set_config_values(host_data[hostname], grp, var_data)
        return host_data


    def get_host_ips(self, host_data):
        return host_data.keys()

    def get_inventory(self, topo, layout, config):
        if len(topo['os_server_res']) == 0:
            return ""
        host_data = self.get_host_data(topo, config)
        inven_hosts = self.get_host_ips(host_data)
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
