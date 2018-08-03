#!/usr/bin/env python


def filter_list_by_attr(output, attr):
    new_output = []
    for ele in output:
        if attr in ele:
            new_output.append(ele)
    return new_output


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'filter_list_by_attr': filter_list_by_attr
        }
