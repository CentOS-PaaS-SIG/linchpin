#!/usr/bin/env python

# flake8: noqa

from nose.tools import assert_equal

import linchpin.InventoryFilters
from linchpin.InventoryFilters import InventoryProviders

from linchpin.InventoryFilters.AWSInventory import AWSInventory
from linchpin.InventoryFilters.BeakerInventory import BeakerInventory
from linchpin.InventoryFilters.DuffyInventory import DuffyInventory
from linchpin.InventoryFilters.DummyInventory import DummyInventory
from linchpin.InventoryFilters.GCloudInventory import GCloudInventory
from linchpin.InventoryFilters.LibvirtInventory import LibvirtInventory
from linchpin.InventoryFilters.OpenstackInventory import OpenstackInventory
from linchpin.InventoryFilters.OvirtInventory import OvirtInventory

def test_get_driver():
    driver = InventoryProviders.get_driver("aws")
    assert_equal(driver, AWSInventory)

def test_get_all_drivers():
    drivers = {
        "aws": AWSInventory,
        "beaker": BeakerInventory,
        "duffy": DuffyInventory,
        "dummy": DummyInventory,
        "gcloud": GCloudInventory,
        "libvirt": LibvirtInventory,
        "openstack": OpenstackInventory,
        "ovirt": OvirtInventory,
    }
    if_drivers = InventoryProviders.get_all_drivers()
    assert_equal(drivers,if_drivers)