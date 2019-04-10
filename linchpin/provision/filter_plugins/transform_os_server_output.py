#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as fil_utils


class FilterModule(object):
    ''' A filter fix distiller '''
    def filters(self):
        return {
            'transform_os_server_output': fil_utils.transform_os_server_output
        }
