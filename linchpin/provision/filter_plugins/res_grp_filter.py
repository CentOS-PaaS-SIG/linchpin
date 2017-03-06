#!/usr/bin/env python
import os
import sys
import abc
import StringIO
from ansible import errors

def filter_groups(resource_group_types, resource_groups, *args):
    output = {}
    for group_type in resource_group_types:
        output[group_type] = []
        for group in resource_groups:
            for arg in args:
                if (arg in group) and (group[arg] == group_type):
                        output[group_type].append(group)
    return output

class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'res_grp_filter': filter_groups
        }
