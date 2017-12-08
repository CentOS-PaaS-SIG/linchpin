#!/usr/bin/env python

from camel import Camel


def to_ordered_dict(data):
    return Camel().dump(data["inventory_layout"])


class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        return {
            'ordered_yaml': to_ordered_dict
        }
