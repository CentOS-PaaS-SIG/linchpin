#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to filter list by attribute '''
    def filters(self):
        return {
            'filter_list_by_attr': filter_utils.filter_list_by_attr
        }
