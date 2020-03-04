#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to write variables to file '''
    def filters(self):
        return {
            'write_to_file': filter_utils.write_to_file
        }
