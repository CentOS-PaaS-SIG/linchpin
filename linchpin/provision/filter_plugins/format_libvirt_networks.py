#!/usr/bin/env python


def format_libvirt_networks(networks,):
    output = ""
    for network in networks:
        output += " --network " + network.get('name', 'default')
    return output


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'format_libvirt_networks': format_libvirt_networks
        }
