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
from InventoryFilters import OpenstackInventory

class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        inv = OpenstackInventory.OpenstackInventory()
        return {
            'os_inv': inv.get_inventory
        }
