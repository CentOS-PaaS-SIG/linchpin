#!/usr/bin/env python
import os

def provide_default(fetched, default):
    if fetched == "":
        return default
    else:
        return fetched

class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        return {
            'provide_default': provide_default
        }
