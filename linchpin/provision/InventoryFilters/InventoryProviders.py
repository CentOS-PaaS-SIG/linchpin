"""
Inventory Providers List
"""

from AWSInventory import AWSInventory
from BeakerInventory import BeakerInventory
from DuffyInventory import DuffyInventory
from DummyInventory import DummyInventory
from GCloudInventory import GCloudInventory
from InventoryFilter import InventoryFilter
from LibvirtInventory import LibvirtInventory
from OpenstackInventory import OpenstackInventory

filter_classes = {
           "aws_inv": AWSInventory,
           "beaker_inv": BeakerInventory,
           "duffy_inv": DuffyInventory,
           "dummy_inv": DummyInventory,
           "gcloud_inv": GCloudInventory,
           "libvirt_inv": LibvirtInventory,
           "os_inv": OpenstackInventory,
}


def get_driver(provider):
    try:
        filter_class = filter_classes[provider]
    except KeyError:
        print("key not found in dictionary")
    return filter_classes[provider]


def get_all_drivers():
    return filter_classes
