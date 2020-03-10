#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to translate rule_type '''
    def filters(self):
        return {
            'os_sg_rule_type': filter_utils.translate_ruletype
        }
