#!/usr/bin/env python

import abc
import StringIO
from camel import Camel
from ansible import errors

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from AWSInventory import AWSInventory
from BeakerInventory import BeakerInventory
from DuffyInventory import DuffyInventory
from DummyInventory import DummyInventory
from GCloudInventory import GCloudInventory
from InventoryFilter import InventoryFilter
from LibvirtInventory import LibvirtInventory
from OpenstackInventory import OpenstackInventory

from InventoryProviders import get_driver, get_all_drivers


class GenericInventory(InventoryFilter):

    def __init__(self):
        InventoryFilter.__init__(self)
        self.filter_classes = get_all_drivers()

    def get_host_ips(self, topo):
        """
        currently it will return the dict as follows:
        {
        "aws_inv": ["x.x.x.x"],
        "os_inv" :["x.x.x.x","x.x.x.x"],
        "gcloud_inv" : ["x.x.x.x","x.x.x.x"]
        }
        """
        host_ip_dict = {}
        for inv_filter in self.filter_classes:
            ips = self.filter_classes[inv_filter]().get_host_ips(topo)
            host_ip_dict[inv_filter] = ips
        return host_ip_dict

    def get_hosts_by_count(self, host_dict, count):
        """
        currently this function gets all the ips/hostname according to the
        order in which inventories are specified. later can be modified
        to work with user input
        """
        all_hosts = []
        for inv in host_dict:
            all_hosts.extend(host_dict[inv])
        return all_hosts[:count]

    def get_inventory(self, topo, layout):
        layout =  Camel().load(layout)
        # get all the topology host_ips
        host_ip_dict = self.get_host_ips(topo)
        # get the count of all layout hosts needed
        layout_host_count = self.get_layout_hosts(layout)
        # generate hosts list based on the layout host count
        inven_hosts = self.get_hosts_by_count(host_ip_dict, layout_host_count)
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

