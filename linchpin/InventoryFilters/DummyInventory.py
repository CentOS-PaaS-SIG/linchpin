#!/usr/bin/env python

from __future__ import absolute_import

from .InventoryFilter import InventoryFilter


class DummyInventory(InventoryFilter):
    def get_host_data(self, res, cfgs={}):
        """
        Returns a dict of hostnames or IP addresses for use in an Ansible
        inventory file, based on available data. Only a single hostname or IP
        address will be returned per instance, so as to avoid duplicate runs of
        Ansible on the same host via the generated inventory file.

        :param topo:
            linchpin Dummy/nummy resource data

        :param cfgs:
            map of config options from PinFile
        """
        host_data = {}
        var_data = cfgs.get('dummy', {})
        var_data.update(cfgs.get('nummy', {}))
        if var_data is None:
            var_data = {}
            var_data['__IP__'] = '__SELF__'
        for host in res['hosts']:
            host_data[host] = {}
            self.set_config_values(host_data[host], host, res, var_data)
        return host_data


    def set_config_values(self, host_data, host, instance, cfgs={}):
        """
        """
        if cfgs is None:
            return
        if 'hostname' not in list(cfgs.keys()):
            cfgs['hostname'] = '__IP__'
        for var in cfgs.keys():
            if var == 'hostname' and cfgs[var] == '__IP__':
                host_data[cfgs[var]] = host
            else:
                host_data[var] = self.config_value_helper(instance, cfgs[var])
