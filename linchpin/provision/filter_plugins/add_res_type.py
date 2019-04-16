#!/usr/bin/env python


def add_res_type(hosts, res_type):
    new_hosts = []
    for host in hosts:
        host['resource_type'] = res_type
        new_hosts.append(host)
    return new_hosts


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'add_res_type': add_res_type
        }
