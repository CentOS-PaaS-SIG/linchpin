#!/usr/bin/env python

# flake8: noqa

from __future__ import absolute_import
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
from linchpin.InventoryFilters.VMwareInventory import VMwareInventory
from linchpin.InventoryFilters.DockerInventory import DockerInventory
from linchpin.InventoryFilters.AzureInventory import AzureInventory
def test_get_driver():
    driver = InventoryProviders.get_driver("aws_ec2_res")
    assert_equal(driver, AWSInventory)

def test_get_all_drivers():
    drivers = {
        "azure_vm" : AzureInventory,
        "aws_ec2_res": AWSInventory,
        "beaker_res": BeakerInventory,
        "duffy_res": DuffyInventory,
        "dummy_res": DummyInventory,
        "nummy_res": DummyInventory,
        "gcloud_gce_res": GCloudInventory,
        "libvirt_res": LibvirtInventory,
        "os_server_res": OpenstackInventory,
        "ovirt_vms_res": OvirtInventory,
        "vmware_guest_res": VMwareInventory,
        "docker_container_res": DockerInventory,
        "docker_image_res": DockerInventory,
    }
    if_drivers = InventoryProviders.get_all_drivers()
    assert_equal(drivers,if_drivers)
