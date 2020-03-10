#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to differentiate public and private ips '''
    def filters(self):
        return {
            'ip_filter': filter_utils.ip_filter
        }
