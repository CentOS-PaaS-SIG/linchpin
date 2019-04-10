#!/usr/bin/env python
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from .InventoryFilter import InventoryFilter


class OvirtInventory(InventoryFilter):
    # we should find a better set of defaults at some point
    DEFAULT_HOSTNAMES = ['ips.address_v4']


    def get_host_data(self, res, cfgs):
        """
        Returns a dict of hostnames or IP addresses for use in an Ansible
        inventory file, based on available data. Only a single hostname or IP
        address will be returned per instance, so as to avoid duplicate runs of
        Ansible on the same host via the generated inventory file.

        Each hostname contains mappings of any variable that was defined in the
        cfgs section of the PinFile (e.g. __IP__) to the value in the field that
        corresponds with that variable in the cfgs.

        By default, the hostname will be the system field returned by ovirt

        :param topo:
            linchpin oVirt resource data

        :param cfgs:
            map of config options from PinFile
        """

        host_data = {}
        if res['resource_type'] != 'ovirt_vms_res':
            return host_data
        var_data = cfgs.get('ovirt', {})
        if var_data is None:
            var_data = {}
        if res['vm']['reported_devices']:
            for dev in res['vm']['reported_devices']:
                host = self.get_hostname(dev, var_data,
                                         self.DEFAULT_HOSTNAMES)
                hostname_var = host[0]
                hostname = host[1]
                host_data[hostname] = {}
                if '__IP__' not in var_data.keys():
                    var_data['__IP__'] = hostname_var
                    host_data[hostname] = {}
                self.set_config_values(host_data[hostname], dev, var_data)
        return host_data

    def get_host_ips(self, host_data):
        return host_data.keys()


    def config_value_helper(self, instance, keys):
        if "." in keys:
            key, rest = keys.split('.', 1)
            # this handles errors in which the key does not exist
            if isinstance(instance, list) and key.isdigit():
                return self.config_value_helper(instance[int(key)], rest)
            if key not in instance.keys():
                return ''
            return self.config_value_helper(instance[key], rest)
        else:
            if keys == '':
                return ''
            elif keys == 'address_v4':
                for addr in instance:
                    if addr['version'] == 'v4':
                        return addr['address']
            elif keys == 'address_v6':
                for addr in instance:
                    if addr['version'] == 'v6':
                        return addr['address']
            elif keys not in instance.keys():
                return ''
            return instance[keys]


    def get_hostname(self, data, cfgs, default_fields):
        if '__IP__' in cfgs.keys():
            val = self.config_value_helper(data, cfgs['__IP__'])
            if val:
                return (cfgs['__IP__'], val)
        for var in default_fields:
            val = self.config_value_helper(data, var)
            if val:
                return (var, val)
        return ''


    def get_inventory(self, topo, layout, config):
        host_data = []
        inven_hosts = []
        for res in topo:
            hd = self.get_host_data(res, config)
            if hd:
                host_data.append(hd)
            inven_hosts = self.get_host_ips(hd)
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
        output = StringIO()
        self.config.write(output)
        return output.getvalue()
