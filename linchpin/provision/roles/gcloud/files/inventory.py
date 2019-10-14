#!/usr/bin/env python

from __future__ import absolute_import
from collections import OrderedDict

from linchpin.InventoryFilters.InventoryFilter import InventoryFilter


class Inventory(InventoryFilter):
    DEFAULT_HOSTNAMES = ['public_ip']

    def get_host_data(self, res, cfgs):
        """
        Returns a dict of hostnames or IP addresses for use in an Ansible
        inventory file, based on available data. Only a single hostname or IP
        address will be returned per instance, so as to avoid duplicate runs of
        Ansible on the same host via the generated inventory file.

        Each hostname contains mappings of any variable that was defined in the
        cfgs section of the PinFile (e.g. __IP__) to the value in the field that
        corresponds with that variable in the cfgs.

        By default, the hostname will be the public_ip field returned by gcloud

        :param topo:
            linchpin GCloud resource data

        :param cfgs:
            map of config options from PinFile
        """
        if res['resource_group'] != 'gcloud':
            return OrderedDict()

        if res['role'] == 'gcloud_gce':
            return self.get_gcloud_gce_host_data(res, cfgs)
        else:
            return OrderedDict()

    def get_gcloud_gce_host_data(self, res, cfgs):
        host_data = OrderedDict()

        var_data = cfgs.get('gcloud', {})
        if var_data is None:
            var_data = {}
        for instance in res['instance_data']:
            host = self.get_hostname(instance, var_data,
                                     self.DEFAULT_HOSTNAMES)
            hostname_var = host[0]
            hostname = host[1]
            host_data[hostname] = {}
            if '__IP__' not in list(var_data.keys()):
                var_data['__IP__'] = hostname_var
                host_data[hostname] = {}
            self.set_config_values(host_data[hostname], instance, var_data)
        return host_data
