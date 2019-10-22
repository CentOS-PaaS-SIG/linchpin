"""
Inventory Providers List
"""
from __future__ import absolute_import
from linchpin.exceptions import LinchpinError
from .JSONInventoryFormatter import JSONInventoryFormatter
from .CFGInventoryFormatter import CFGInventoryFormatter

formatter_classes = {
    "cfg": CFGInventoryFormatter,
    "ini": CFGInventoryFormatter,
    "json": JSONInventoryFormatter
}


def get_inv_formatter(inv_type):
    if inv_type not in formatter_classes:
        raise LinchpinError("Key {0} not found in"
                            " formatters".format(inv_type))
    return formatter_classes[inv_type]


def get_all_inv_formatters():
    return formatter_classes
