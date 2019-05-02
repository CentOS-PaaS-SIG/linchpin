#!/usr/bin/env python

from __future__ import absolute_import
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to fix unicode format '''
    def filters(self):
        return {
            'unicode_filter': filter_utils.unicode_filter
        }
