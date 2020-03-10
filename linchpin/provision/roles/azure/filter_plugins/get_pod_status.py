#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to get pod status '''
    def filters(self):
        return {
            'get_pod_status': filter_utils.get_pod_status
        }
