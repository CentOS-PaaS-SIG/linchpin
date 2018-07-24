#!/usr/bin/env python

import StringIO

from InventoryFilter import InventoryFilter


class AWSInventory(InventoryFilter):

    def get_host_ips(self, topo):
        """
        Returns a list of hostnames or IP addresses for use in an Ansible
        inventory file, based on available data. Only a single hostname or IP
        address will be returned per instance, so as to avoid duplicate runs of
        Ansible on the same host via the generated inventory file.

        If an instance has a public IP attached, its hostname in DNS will be
        returned if available, and if not the public IP address will be used.
        For instances which have a private IP address for VPC use cases, the
        private IP address will be returned since private EC2 hostnames (e.g.
        ip-10-0-0-1.ec2.internal) will not typically be resolvable outside of
        AWS. For instances with both a public and private IP address, the
        public address is always returned instead of the private address.

        :param topo:
            linchpin AWS EC2 resource data
        """

        host_dns_ip = []
        for group in topo['aws_ec2_res']:
            for instance in group['instances']:
                if instance['public_dns_name']:
                    host_dns_ip.append(str(instance['public_dns_name']))
                elif instance['public_ip']:
                    host_dns_ip.append(str(instance['public_ip']))
                else:
                    host_dns_ip.append(str(instance['private_ip']))
        return host_dns_ip

    def get_inventory(self, topo, layout):

        if len(topo['aws_ec2_res']) == 0:
            return ""
        inven_hosts = self.get_host_ips(topo)
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
