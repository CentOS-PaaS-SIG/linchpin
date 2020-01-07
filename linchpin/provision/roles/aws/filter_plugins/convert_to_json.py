#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to convert string to json '''
    def filters(self):
        return {
            'convert_to_json': filter_utils.convert_to_json
        }
