#!/usr/bin/env python

# flake8: noqa

import os
import sys

def get_ip_arp(text, mac):
    # "mac address='52:54:00:cb:8a:d7'/>"
    for line in text:
        if mac in line:
            return line.split("(")[1].split(")")[0]
    return mac

class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        return {
            'get_ip_arp': get_ip_arp
        }
