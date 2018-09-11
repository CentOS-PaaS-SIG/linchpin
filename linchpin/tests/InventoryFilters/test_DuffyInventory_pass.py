#!/usr/bin/env python

# flake8: noqa

import os
import json
import yaml

from nose.tools import *

from linchpin.InventoryFilters import DuffyInventory

def setup_duffy_inventory_filter():
    global filter
    global topo

    filter = DuffyInventory.DuffyInventory()
    
    provider = 'general'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    topology = 'topo.json'
    topo_file = open(mock_path+'/'+topology)
    topo = json.load(topo_file)
    topo_file.close()

def setup_duffy_layout():
    global layout

    provider = 'layouts'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    template = 'parsed-layout.json'
    template_file = open(mock_path+'/'+template)
    layout = json.load(template_file)

@with_setup(setup_duffy_inventory_filter)
def test_get_hostnames():
    """
    """
    hostnames = filter.get_hostnames(topo)
    expected_hosts = ['109.254.93.117', 'test.example.com', '171.109.242.199']
    assert_equal(set(hostnames), set(expected_hosts))

@with_setup(setup_duffy_inventory_filter)
def test_get_host_ips():
    """
    """
    ips = filter.get_host_ips(topo)
    expected_hosts = ['109.254.93.117', 'test.example.com', '171.109.242.199']
    assert_equal(set(ips), set(expected_hosts))

@with_setup(setup_duffy_inventory_filter)
@with_setup(setup_duffy_layout)
def test_get_inventory():
    """
    """
    empty_topo = dict()
    empty_topo['duffy_res'] = []
    inventory = filter.get_inventory(empty_topo, layout)
    # should return an empty string
    assert_false(inventory)
    inventory = filter.get_inventory(topo, layout)
    # should return some data
    assert_true(inventory)