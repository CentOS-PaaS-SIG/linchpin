#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to add_res_data '''
    def filters(self):
        return {
            'add_res_data': filter_utils.add_res_data
        }
