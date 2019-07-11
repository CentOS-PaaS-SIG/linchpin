#!/usr/bin/env python

from __future__ import absolute_import
from collections import OrderedDict

from .InventoryFilter import InventoryFilter


class DuffyInventory(InventoryFilter):
    def get_host_data(self, res, cfgs):
        """
        Returns a dict of hostnames or IP addresses for use in an Ansible
        inventory file, based on available data. Only a single hostname or IP
        address will be returned per instance, so as to avoid duplicate runs of
        Ansible on the same host via the generated inventory file.

        Each hostname contains mappings of any variable that was defined in the
        cfgs section of the PinFile (e.g. __IP__) to the value in the field that
        corresponds with that variable in the cfgs.

        By default, the hostname will be the system field returned by duffy

        :param topo:
            linchpin Duffy resource data

        :param cfgs:
            map of config options from PinFile
        """
        host_data = OrderedDict()
        if res['resource_type'] != 'duffy_res':
            return host_data
        var_data = cfgs.get('duffy', {})
        if var_data is None:
            var_data = {}
        for host in res['hosts']:
            host_data[host] = {}
            if '__IP__' not in list(var_data.keys()):
                host_data[host]['__IP__'] = host
            self.set_config_values(host_data[host], res, var_data)
        return host_data
