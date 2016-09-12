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
sys.path.append(os.getcwd())
from InventoryFilters import GCloudInventory

class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        inv = GCloudInventory.GCloudInventory()
        return {
            'gcloud_inv': inv.get_inventory
        }
