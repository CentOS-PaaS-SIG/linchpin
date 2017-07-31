#!/usr/bin/env python

import os
import sys


filepath = os.path.realpath(__file__)
filepath = "/".join(filepath.split("/")[0:-2])
sys.path.append(filepath)

from InventoryFilters import DuffyInventory  # noqa


class FilterModule(object):
    ''' A filter to fix interface's name format '''

    def filters(self):

        inv = DuffyInventory.DuffyInventory()
        return {
            'duffy_inv': inv.get_inventory
        }
