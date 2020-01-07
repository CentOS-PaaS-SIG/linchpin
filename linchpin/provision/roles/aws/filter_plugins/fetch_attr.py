#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to fetch ann attr from dict '''
    def filters(self):
        return {
            'fetch_attr': filter_utils.fetch_attr
        }
