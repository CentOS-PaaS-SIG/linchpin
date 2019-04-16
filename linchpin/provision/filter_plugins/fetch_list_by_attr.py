#!/usr/bin/env python


def fetch_list_by_attr(output, attr):
    new_output = []
    for ele in output:
        if attr in ele:
            new_output.append(ele[attr])
    return new_output


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'fetch_list_by_attr': fetch_list_by_attr
        }
