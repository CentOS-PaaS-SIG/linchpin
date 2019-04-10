#!/usr/bin/env python


def format_output(output, omit):
    if output == "":
        return omit
    return output


class FilterModule(object):
    ''' A filter to fix output format '''
    def filters(self):
        return {
            'omit_filter': format_output
        }
