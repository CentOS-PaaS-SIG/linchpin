#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to format_output with omit '''
    def filters(self):
        return {
            'omit_filter': filter_utils.format_output
        }
