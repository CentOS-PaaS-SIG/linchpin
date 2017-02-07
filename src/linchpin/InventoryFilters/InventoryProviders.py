"""
Inventory Providers List
"""

from AWSInventory import AWSInventory
from OpenstackInventory import OpenstackInventory
from GCloudInventory import GCloudInventory
from DuffyInventory import DuffyInventory
from BeakerInventory import BeakerInventory
from LibvirtInventory import LibvirtInventory
from InventoryFilter import InventoryFilter

filter_classes = {
           "aws_inv": AWSInventory,
           "os_inv": OpenstackInventory,
           "gcloud_inv": GCloudInventory,
           "duffy_inv": DuffyInventory,
           "beaker_inv": BeakerInventory,
           "libvirt_inv": LibvirtInventory
}


def get_driver(provider):
    try:
        filter_class = filter_classes[provider]
    except KeyError:
        print("key not found in dictionary")
    return filter_classes[provider]


def get_all_drivers():
    return filter_classes
