#!/usr/bin/env python


def fetch_attr(output_dict, attr, default):
    return output_dict.get(attr, default)


class FilterModule(object):
    ''' A filter to fetch ann attr from dict '''
    def filters(self):
        return {
            'fetch_attr': fetch_attr
        }
