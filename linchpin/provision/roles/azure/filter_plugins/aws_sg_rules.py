#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to format AWS EC2 security group rules '''
    def filters(self):
        return {
            'aws_sg_rules': filter_utils.format_rules
        }
