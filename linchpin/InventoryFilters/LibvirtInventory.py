#!/usr/bin/env python

from __future__ import absolute_import

from .InventoryFilter import InventoryFilter


class LibvirtInventory(InventoryFilter):
    DEFAULT_HOSTNAMES = ['ip']


    def get_host_data(self, res, cfgs):
        """
        Returns a dict of hostnames or IP addresses for use in an Ansible
        inventory file, based on available data. Only a single hostname or IP
        address will be returned per instance, so as to avoid duplicate runs of
        Ansible on the same host via the generated inventory file.

        Each hostname contains mappings of any variable that was defined in the
        cfgs section of the PinFile (e.g. __IP__) to the value in the field that
        corresponds with that variable in the cfgs.

        By default, the hostname will be the system field returned by libvirt

        :param topo:
            linchpin Libvirt resource data

        :param cfgs:
            map of config options from PinFile
        """

        host_data = {}
        if res['resource_type'] != 'libvirt_res':
            return host_data
        var_data = cfgs.get('libvirt', {})
        if var_data is None:
            var_data = {}
        host = self.get_hostname(res, var_data,
                                 self.DEFAULT_HOSTNAMES)
        hostname_var = host[0]
        hostname = host[1]
        host_data[hostname] = {}
        if '__IP__' not in list(var_data.keys()):
            var_data['__IP__'] = hostname_var
            host_data[hostname] = {}
        host_data[hostname] = {}
        self.set_config_values(host_data[hostname], res, var_data)
        return host_data
