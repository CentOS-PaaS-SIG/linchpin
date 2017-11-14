#!/usr/bin/env python


def get_host_from_uri(uri):
    """
    examples: qemu+ssh://root@hail.cloud.example.com/system
              test:///default
              qemu+ssh://192.168.122.6/system
    """
    uri = uri.split("//")[-1].split("/")[0].split("@")[-1]
    if uri == '':
        return 'localhost'
    return uri


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'get_host_from_uri': get_host_from_uri
        }
