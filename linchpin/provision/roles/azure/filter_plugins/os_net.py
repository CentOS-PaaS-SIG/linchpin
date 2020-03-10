#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'os_net': filter_utils.format_networks
        }
