#!/usr/bin/env python

from __future__ import print_function
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'map_results': filter_utils.map_results
        }
