#!/usr/bin/env python

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from .InventoryFilter import InventoryFilter


class AWSInventory(InventoryFilter):
    DEFAULT_HOSTNAMES = ['public_dns_name', 'public_ip', 'private_ip']

    def get_host_data(self, res, cfgs):
        """
        Returns a dict of hostnames or IP addresses for use in an Ansible
        inventory file, based on available data. Only a single hostname or IP
        address will be returned per instance, so as to avoid duplicate runs of
        Ansible on the same host via the generated inventory file.

        Each hostname contains mappings of any variable that was defined in the
        cfgs section of the PinFile (e.g. __IP__) to the value in the field that
        corresponds with that variable in the cfgs.

        If an instance has a public IP attached, its hostname in DNS will be
        returned if available, and if not the public IP address will be used.
        For instances which have a private IP address for VPC use cases, the
        private IP address will be returned since private EC2 hostnames (e.g.
        ip-10-0-0-1.ec2.internal) will not typically be resolvable outside of
        AWS. For instances with both a public and private IP address, the
        public address is always returned instead of the private address.

        :param topo:
            linchpin AWS EC2 resource data

        :param cfgs:
            map of config options from PinFile
        """

        host_data = {}
        if res['resource_type'] != 'aws_ec2_res':
            return host_data
        var_data = cfgs.get('aws', {})
        if var_data is None:
            var_data = {}
        for instance in res['instances']:
            host = self.get_hostname(instance, var_data,
                                     self.DEFAULT_HOSTNAMES)
            hostname_var = host[0]
            hostname = host[1]
            if '__IP__' not in var_data.keys():
                var_data['__IP__'] = hostname_var
            host_data[hostname] = {}
            self.set_config_values(host_data[hostname], instance, var_data)
        return host_data

    def get_host_ips(self, host_data):
        if host_data:
            return host_data.keys()
        else:
            return []

    def get_inventory(self, topo, layout, config):
        host_data = []
        inven_hosts = []
        for res in topo:
            hd = self.get_host_data(res, config)
            if hd:
                host_data.append(hd)
            inven_hosts.extend(self.get_host_ips(hd))
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
