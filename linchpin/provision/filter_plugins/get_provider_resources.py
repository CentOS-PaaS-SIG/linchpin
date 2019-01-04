#!/usr/bin/env python


def get_provider_resources(topo_output, res_type):
    provider_resources = []
    for host in topo_output:
        if host['resource_type'] == res_type:
            provider_resources.append(host)
    return provider_resources


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'get_provider_resources': get_provider_resources
        }
