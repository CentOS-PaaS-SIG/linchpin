#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to provide default value when not given '''
    def filters(self):
        return {
            'provide_default': filter_utils.provide_default
        }
