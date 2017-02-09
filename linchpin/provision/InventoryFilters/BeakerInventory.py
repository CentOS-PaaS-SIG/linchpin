try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from InventoryFilter import InventoryFilter

class BeakerInventory(InventoryFilter):

    def get_hostnames(self, topology):
        hostnames = []
        if not ('beaker_res' in topology):
            return hostnames
        for group in topology['beaker_res']:
            hostnames.append(group['system'])
        return hostnames

    def get_host_ips(self, topo):
        return self.get_hostnames(topo)

    def add_hosts_to_groups(self, config, inven_hosts, layout):
        pass

    def get_inventory(self, topo, layout):
        if not ('beaker_res' in topo):
            return ''
        if len(topo['beaker_res']) == 0:
            return ''
        inven_hosts = self.get_host_ips(topo)
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
