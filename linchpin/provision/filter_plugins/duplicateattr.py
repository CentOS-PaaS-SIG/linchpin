#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to filter duplicate attributes '''
    def filters(self):
        return {
            'duplicateattr': filter_utils.duplicateattr
        }
