#!/usr/bin/env python

import json


def fetch_attr(output_dict, attr, default):
    return output_dict.get(attr, default)


class FilterModule(object):
    ''' A filter to fetch from dict '''
    def filters(self):
        return {
            'fetch_attr': fetch_attr
        }
