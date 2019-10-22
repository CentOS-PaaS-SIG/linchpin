#!/usr/bin/env python

import imp
import os

from .InventoryFilter import InventoryFilter
from .InventoryProviders import get_inv_formatter


class GenericInventory(InventoryFilter):

    def __init__(self, inv_format="cfg", pb_path=None):
        InventoryFilter.__init__(self)
        self.pb_path = pb_path
        self.inv_formatter = get_inv_formatter(inv_format)()

    def get_host_data(self, res_output, config):
        """
        """
        host_data = []
        for res_grp in res_output:
            res_type = res_grp['resource_group']
            # check only when the inventory_filter exists
            filter_class = self.get_filter_class(res_type)
            data = filter_class.get_host_data(res_grp, config)
            host_data.append(data)
        return host_data


    def get_filter_class(self, res_type):
        path = "{0}/files/inventory.py".format(self._find_role_path(res_type))
        provider = imp.load_source('Inventory', path)
        return provider.Inventory()


    def _find_role_path(self, res_type):
        """
        returns the full path to the given playbook

        :params res_type: name of the role
        """

        for path in self.pb_path:
            p = '{0}/{1}/{2}'.format(path, 'roles', res_type)

            if os.path.exists(os.path.expanduser(p)):
                return p


    def get_hosts_by_count(self, host_data, count):
        """
        currently this function gets all the ips/hostname according to the
        order in which inventories are specified. later can be modified
        to work with user input
        """

        all_hosts = []
        for host in host_data:
            all_hosts.extend(list(host.keys()))
        return all_hosts[:count]

    def populate_config(self, host_dict, res_output, config):
        """
        """
        populated_config = {}
        for provider in host_dict.keys():
            for host in host_dict[provider].keys():
                populated_config[host] = {}
                for var in config[provider]:
                    value = self.filter_classes[provider]().\
                        get_field_values(res_output, var)
                    populated_config[host][var] = value
        return populated_config

    def get_inventory(self, res_output, layout, topology, config):
        # get all the topology host_ips
        host_data = self.get_host_data(res_output, config)
        # sort it based on topology
        # get the count of all layout hosts needed
        layout_host_count = self.get_layout_hosts(layout)
        # generate hosts list based on the layout host count
        inven_hosts = self.get_hosts_by_count(host_data,
                                              layout_host_count)
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
        self.inv_formatter.add_common_vars(host_groups, layout, host_data)
        return self.inv_formatter.generate_inventory()
