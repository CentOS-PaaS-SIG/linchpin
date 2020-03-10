#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to get os_server_names from outputs '''
    def filters(self):
        return {
            'fetch_os_server_names': filter_utils.get_os_server_names
        }
