#!/usr/bin/env python
import os
import sys
import abc
import StringIO
from ansible import errors
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


filepath = os.path.realpath(__file__)
filepath = "/".join(filepath.split("/")[0:-2])
sys.path.append(filepath)


from InventoryFilters import AWSInventory

class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        inv = AWSInventory.AWSInventory()
        return {
            'aws_inv': inv.get_inventory
        }
