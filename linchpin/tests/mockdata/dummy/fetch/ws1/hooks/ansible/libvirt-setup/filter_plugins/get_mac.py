#!/usr/bin/env python

# flake8: noqa

import os
import sys

def get_mac_fun(text):
    # "mac address='52:54:00:cb:8a:d7'/>"
    strn = text[0]
    return strn.split("=")[-1].strip("'").strip("'/>")

class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        return {
            'get_mac': get_mac_fun
        }
