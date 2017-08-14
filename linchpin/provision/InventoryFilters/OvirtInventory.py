#!/usr/bin/env python
import StringIO

from InventoryFilter import InventoryFilter


class OvirtInventory(InventoryFilter):

    def get_host_ips(self, topo):
        host_public_ips = []
        for vm in topo['ovirt_vms_res']:
            if vm['vm']['reported_devices']:
                for dev in vm['vm']['reported_devices']:
                    for ip in dev.get('ips', []):
                        if ip['version'] == 'v4':
                            host_public_ips.append(ip['address'])
                            break
            else:
                host_public_ips.append('')
        return host_public_ips

    def get_inventory(self, topo, layout):

        if len(topo['ovirt_vms_res']) == 0:
            return ""
        # no_of_groups = len(topo['ovirt_vms_res'])
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
