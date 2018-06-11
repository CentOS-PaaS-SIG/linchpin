"""
Inventory Providers List
"""
from linchpin.exceptions import LinchpinError

from AWSInventory import AWSInventory
from BeakerInventory import BeakerInventory
from DuffyInventory import DuffyInventory
from DummyInventory import DummyInventory
from GCloudInventory import GCloudInventory
from LibvirtInventory import LibvirtInventory
from OpenstackInventory import OpenstackInventory
from OvirtInventory import OvirtInventory

from CFGInventoryFormatter import CFGInventoryFormatter
from JSONInventoryFormatter import JSONInventoryFormatter

filter_classes = {
    "aws_inv": AWSInventory,
    "beaker_inv": BeakerInventory,
    "duffy_inv": DuffyInventory,
    "dummy_inv": DummyInventory,
    "gcloud_inv": GCloudInventory,
    "libvirt_inv": LibvirtInventory,
    "os_inv": OpenstackInventory,
    "ovirt_inv": OvirtInventory,
}

formatter_classes = {
    "cfg": CFGInventoryFormatter,
    "ini": CFGInventoryFormatter,
    "json": JSONInventoryFormatter
}


def get_driver(provider):

    if provider not in filter_classes:
            raise LinchpinError("Key {0} not found in"
                                " inventory provider dict".format(provider))

    return filter_classes[provider]


def get_all_drivers():
    return filter_classes


def get_inv_formatter(inv_type):
    if inv_type not in formatter_classes:
            raise LinchpinError("Key {0} not found in"
                                " formatters".format(inv_type))
    return formatter_classes[inv_type]


def get_all_inv_formatters():
    return formatter_classes
