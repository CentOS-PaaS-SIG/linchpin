#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to get provider resources '''
    def filters(self):
        return {
            'get_provider_resources': filter_utils.get_provider_resources
        }
