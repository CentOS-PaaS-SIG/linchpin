#!/usr/bin/env python

# flake8: noqa

import os
import json
import yaml

from nose.tools import *

from linchpin.InventoryFilters import LibvirtInventory

def setup_libvirt_inventory_filter():
    global filter
    global topo

    filter = LibvirtInventory.LibvirtInventory()

    provider = 'general-inventory'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    topology = 'linchpin.benchmark'
    topo_file = open(mock_path+'/'+topology)
    topo = json.load(topo_file)['17']['targets'][0]['general-inventory']['outputs']['resources']
    topo_file.close()


def setup_libvirt_config():
    global config

    provider = 'general-inventory'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    cfg = 'PinFile'
    cfg_file = open(mock_path+'/'+cfg)
    config = yaml.load(cfg_file)['general-inventory']['cfgs']
    cfg_file.close()


def setup_libvirt_layout():
    global layout

    provider = 'general-inventory'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    template = 'linchpin.benchmark'
    template_file = open(mock_path+'/'+template)
    layout = json.load(template_file)['17']['targets'][0]['general-inventory']['inputs']['layout_data']['inventory_layout']


@with_setup(setup_libvirt_inventory_filter)
@with_setup(setup_libvirt_config)
def test_get_host_data():
    """
    """
    host_data = filter.get_host_data(topo[3], config)
    expected_vars = ['__IP__']
    for host in host_data:
        assert_equal(set(host_data[host].keys()), set(expected_vars))


@with_setup(setup_libvirt_inventory_filter)
@with_setup(setup_libvirt_config)
def test_get_host_ips():
    """
    """
    host_data = filter.get_host_data(topo[3], config)
    ips = filter.get_host_ips(host_data)
    expected_hosts = ["192.168.122.219"]
    assert_equal(set(host_data.keys()), set(expected_hosts))


@with_setup(setup_libvirt_inventory_filter)
@with_setup(setup_libvirt_config)
@with_setup(setup_libvirt_layout)
def test_get_inventory():
    """
    """
    inventory = filter.get_inventory(topo, layout, config)
    assert_true(inventory)
