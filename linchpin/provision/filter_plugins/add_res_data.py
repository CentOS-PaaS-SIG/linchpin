#!/usr/bin/env python
#import linchpin.FilterUtils.FilterUtils as filter_utils

def add_res_data(hosts, res_grp, role):
    new_hosts = []
    for host in hosts:
        host['resource_group'] = res_grp
        host['role'] = role
        new_hosts.append(host)
    return new_hosts


class FilterModule(object):
    ''' A filter to add_res_data '''
    def filters(self):
        return {
            'add_res_data': add_res_data
        }
