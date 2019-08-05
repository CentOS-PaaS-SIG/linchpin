#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to fetch vm/instance names from topology outputs '''
    def filters(self):
        return {
            'fetch_vm_names': filter_utils.fetch_vm_names
        }
