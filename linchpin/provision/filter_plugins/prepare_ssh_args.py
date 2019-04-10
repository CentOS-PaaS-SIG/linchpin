#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to prepare ssh args '''
    def filters(self):
        return {
            'prepare_ssh_args': filter_utils.prepare_ssh_args
        }
