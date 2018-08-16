#!/usr/bin/env python

# flake8: noqa

import os
import json
import yaml

from nose.tools import *

from linchpin.InventoryFilters import OpenstackInventory

def setup_openstack_inventory_filter():
    global filter
    global topo

    filter = OpenstackInventory.OpenstackInventory()
    
    provider = 'general'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    topology = 'topo.json'
    topo_file = open(mock_path+'/'+topology)
    topo = json.load(topo_file)
    topo_file.close()

def setup_openstack_layout():
    global layout

    provider = 'layouts'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    template = 'parsed-layout.json'
    template_file = open(mock_path+'/'+template)
    layout = json.load(template_file)

@with_setup(setup_openstack_inventory_filter)
def test_get_host_ips():
    """
    """
    ips = filter.get_host_ips(topo)
    expected_hosts = ["204.36.91.83", "93.68.5.129", "174.82.209.133"]
    assert_equal(set(ips), set(expected_hosts))

@with_setup(setup_openstack_inventory_filter)
@with_setup(setup_openstack_layout)
def test_get_inventory():
    """
    """
    empty_topo = dict()
    empty_topo['os_server_res'] = []
    inventory = filter.get_inventory(empty_topo, layout)
    assert_false(inventory)
    inventory = filter.get_inventory(topo, layout)
    assert_true(inventory)