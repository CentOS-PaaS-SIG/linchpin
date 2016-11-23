#!/usr/bin/env python

from ansible import errors
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
import StringIO
import pprint


def get_host_ips(topo):
    host_public_ips = []
    for group in topo['aws_ec2_res']:
        for instance in group['instances']:
            host_public_ips.append(str(instance['public_dns_name']))
    return host_public_ips


def get_layout_hosts(inv):
    return inv['hosts'].keys()


def get_layout_host_groups(inv):
    return inv['host_groups'].keys()


def add_sections(config, section_list):
    for section in section_list:
        config.add_section(section)
    return config


def set_children(config, inv):
    for host_group in inv['host_groups']:
        if "children" in inv['host_groups'][host_group]:
            config.add_section(host_group + ":" + "children")
            for child in inv['host_groups'][host_group]['children']:
                config.set(host_group + ":" + "children", child)
    return config


def set_vars(config, inv):
    for host_group in inv['host_groups']:
        if "vars" in inv['host_groups'][host_group]:
            config.add_section(host_group + ":" + "vars")
            for var in inv['host_groups'][host_group]['vars']:
                config.set(host_group + ":" + "vars",
                           var,
                           inv['host_groups'][host_group]['vars'][var])
    return config


def add_ips_to_groups(config, inven_hosts, layout):
    # create a ip to host mapping based on count
    ip_to_host = {}
    for host_name in layout['hosts']:
        count = layout['hosts'][host_name]['count']
        host_list = []
        for i in range(0, count):
            item = inven_hosts.pop()
            host_list.append(item)
        ip_to_host[host_name] = host_list
    # add ips to the host groups in inventory
    for host_name in layout['hosts']:
        host_ips = ip_to_host[host_name]
        for ip in host_ips:
            for host_group in layout['hosts'][host_name]['host_groups']:
                config.set(host_group, ip)
    return config


def add_common_vars(config, host_groups, layout):
    common_vars = layout['vars']
    for group in host_groups:
        items = dict(config.items(group)).keys()
        config.remove_section(group)
        config.add_section(group)
        for item in items:
            host_string = item
            for var in common_vars:
                if common_vars[var] == "__IP__":
                    host_string += " " + var + "=" + item + " "
            config.set(group, host_string)
    return config


def aws_inventory(topo, layout):
    inventory = ConfigParser(allow_no_value=True)
    no_of_groups = len(topo['aws_ec2_res'])
    layout_hosts = get_layout_hosts(layout)
    inven_hosts = get_host_ips(topo)
    # adding sections to respective host groups
    host_groups = get_layout_host_groups(layout)
    inventory = add_sections(inventory, host_groups)
    # set children for each host group
    inventory = set_children(inventory, layout)
    # set vars for each host group
    inventory = set_vars(inventory, layout)
    # add ip addresses to each host
    inventory = add_ips_to_groups(inventory, inven_hosts, layout)
    inventory = add_common_vars(inventory, host_groups, layout)
    output = StringIO.StringIO()
    inventory.write(output)
    return output.getvalue()


class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        return {
            'aws_inventory': aws_inventory
        }
