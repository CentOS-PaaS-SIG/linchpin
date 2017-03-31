#!/usr/bin/env python
import os
import sys
import abc
import StringIO
from ansible import errors

def mapattrs(output, *args):
    mapoutput = []
    for arg in args:
        for ele in output:
            if arg in ele:
                mapoutput.append(ele[arg])
    return list(set(mapoutput))

class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'mapmultipleattr': mapattrs
        }
