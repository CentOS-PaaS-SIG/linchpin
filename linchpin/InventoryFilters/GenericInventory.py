#!/usr/bin/env python

from .InventoryFilter import InventoryFilter
from .InventoryProviders import get_all_drivers
from .InventoryProviders import get_inv_formatter


class GenericInventory(InventoryFilter):

    def __init__(self, inv_format="cfg"):
        InventoryFilter.__init__(self)
        self.filter_classes = get_all_drivers()
        self.inv_formatter = get_inv_formatter(inv_format)()

    def get_host_ips(self, res_output):
        """
        currently it will return the dict as follows:
        {
        "aws": ["x.x.x.x"],
        "os" :["x.x.x.x","x.x.x.x"],
        "gcloud" : ["x.x.x.x","x.x.x.x"]
        }
        """

        host_ip_dict = {}
        for inv_filter in self.filter_classes:
            ips = self.filter_classes[inv_filter]().get_host_ips(res_output)
            host_ip_dict[inv_filter] = ips
        return host_ip_dict

    def get_hosts_by_count(self, host_dict, count, sort_order):
        """
        currently this function gets all the ips/hostname according to the
        order in which inventories are specified. later can be modified
        to work with user input
        """

        all_hosts = []
        for provider in sort_order:
            if isinstance(host_dict[provider], str):
                all_hosts.append(host_dict[provider])
            else:
                all_hosts.extend(host_dict[provider])
        return all_hosts[:count]

    def get_inventory(self, res_output, layout, topology):
        # get the provisioning order
        sort_order = []
        for resource_group in topology["resource_groups"]:
            if not (resource_group.get("resource_group_type") in sort_order):
                sort_order.append(resource_group.get("resource_group_type"))
        # get all the topology host_ips
        host_ip_dict = self.get_host_ips(res_output)
        # sort it based on topology
        # get the count of all layout hosts needed
        layout_host_count = self.get_layout_hosts(layout)
        # generate hosts list based on the layout host count
        inven_hosts = self.get_hosts_by_count(host_ip_dict,
                                              layout_host_count,
                                              sort_order)
        # adding sections to respective host groups
        host_groups = self.get_layout_host_groups(layout)

        self.inv_formatter.add_sections(host_groups)
        # set children for each host group
        self.inv_formatter.set_children(layout)
        # set vars for each host group
        self.inv_formatter.set_vars(layout)
        # add ip addresses to each host
        self.inv_formatter.add_ips_to_groups(inven_hosts, layout)
        # add common vars to host_groups
        self.inv_formatter.add_common_vars(host_groups, layout)
        return self.inv_formatter.generate_inventory()
