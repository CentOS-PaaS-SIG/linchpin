#!/usr/bin/env python


def filter_list_by_attr_val(output, attr, val):
    new_output = []
    for ele in output:
        if attr in ele:
            if ele[attr] == val:
              new_output.append(ele)
    return new_output


class FilterModule(object):
    ''' Filters a list by attr and value of each element '''
    def filters(self):
        return {
            'filter_list_by_attr_val': filter_list_by_attr_val
        }
