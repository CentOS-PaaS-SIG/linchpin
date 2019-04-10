#!/usr/bin/env python


from __future__ import absolute_import
from six.moves import range
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'render_os_server_insts': filter_utils.render_os_server_insts
        }
