#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to get host from libvirt uri '''
    def filters(self):
        return {
            'get_host_from_uri': filter_utils.get_host_from_uri
        }
