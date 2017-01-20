#!/usr/bin/env python
import yaml
import json


def format_output(output):
    output = json.dumps(output)
    return output

class FilterModule(object):
    ''' A filter to fix output format '''
    def filters(self):
        return {
            'unicode_filter': format_output
        }
