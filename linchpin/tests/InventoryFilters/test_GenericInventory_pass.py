#!/usr/bin/env python

# flake8: noqa

from __future__ import print_function
import os
import json
import yaml
import json
import difflib

from configparser import ConfigParser

from nose.tools import *

from linchpin.InventoryFilters import GenericInventory

def setup_generic_inventory_filter():
    global filter
    global res_output

    filter = GenericInventory.GenericInventory()

    provider = 'general-inventory'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    res_output = 'linchpin.benchmark'
    res_file = open(mock_path+'/'+res_output)
    res_output = json.load(res_file)['17']['targets'][0]['general-inventory']['outputs']['resources']
    res_file.close()

def setup_generic_topology():
    global topology

    provider = 'general-inventory'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    topo = 'PinFile'
    topo_file = open(mock_path+'/'+topo)
    topology = yaml.load(topo_file)['general-inventory']['topology']
    topo_file.close()

def setup_generic_config():
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

def setup_generic_layout():
    global layout

    provider = 'general-inventory'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    template = 'linchpin.benchmark'
    template_file = open(mock_path+'/'+template)
    layout = json.load(template_file)['17']['targets'][0]['general-inventory']['inputs']['layout_data']['inventory_layout']

def setup_complex_workspace():
    global workspace

    provider = 'complex-inventory'
    base_path = '{0}'.format(os.path.dirname(
        os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    workspace = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)


@with_setup(setup_generic_inventory_filter)
@with_setup(setup_generic_config)
def test_get_host_data():
    """
    """
    host_data = filter.get_host_data(res_output, config)
    hosts = []
    for data in host_data:
        for host in data:
            assert_true('__IP__' in data[host].keys())
            hosts.append(data[host]['__IP__'])
    expected_hosts = ['10.179.254.83', 'hp-dl380pgen8-02-vm-15.lab.bos.redhat.com', 'dummy-744068-0', 'dummy-744068-1', 'dummy-744068-2', '192.168.122.219', '172.16.100.11', '155.132.55.17', '11.50.197.1', '109.254.93.117', '180.20.194.96', '194.231.24.112', '171.109.242.199', 'test.example.com']
    assert_equal(set(hosts), set(expected_hosts))


@with_setup(setup_generic_inventory_filter)
@with_setup(setup_generic_config)
def test_get_hosts_by_count():
    """
    """
    host_data = filter.get_host_data(res_output, config)
    expected_hosts = ['10.179.254.83', 'hp-dl380pgen8-02-vm-15.lab.bos.redhat.com', 'dummy-744068-2']
    hosts = filter.get_hosts_by_count(host_data, 0)
    assert_equal(len(hosts), 0)
    hosts = filter.get_hosts_by_count(host_data, 3)
    assert_equal(len(hosts), 3)
    assert_equal(set(hosts), set(expected_hosts))


@with_setup(setup_generic_inventory_filter)
@with_setup(setup_generic_topology)
@with_setup(setup_generic_config)
@with_setup(setup_generic_layout)
def test_get_inventory():
    """
    """
    inventory = filter.get_inventory(res_output, layout, topology, config)
    assert_true(inventory)

@with_setup(setup_complex_workspace)
@with_setup(setup_generic_inventory_filter)
@with_setup(setup_generic_config)
def test_output_order():
    """
    Test that inventories are ordered correctly

    This test checks that hosts and variables are ordered correctly when a
    provisioning output made up of multiple hosts is passed to the inventory
    generator.

    input: resources, topology, and layout from a mock succcessful provisioning
    output: an inventory file whose order will be verified
    """

    # get topology and layout
    pf_path = '{0}/{1}'.format(workspace, 'PinFile')
    pinfile = yaml.load(open(pf_path))
    topology = pinfile['complex-inventory']['topology']
    layout_path = '{0}/{1}'.format(workspace, 'layout.json')
    layout = json.load(open(layout_path))

    # get res_output
    output_path = '{0}/{1}'.format(workspace, 'linchpin.benchmark')
    res_output = json.load(open(output_path))
    res_output = res_output[list(res_output.keys())[0]]['targets'][0]['complex-inventory']['outputs']['resources']

    # call get_inventory and print the result
    inventory = filter.get_inventory(res_output, layout, topology, config)

    # load in "correct" inventory file
    correct_inv_path = '{0}/{1}'.format(workspace,
                                            'correct-inventory')
    correct_inventory = open(correct_inv_path, 'r').read()

    # check that the two inventories are equal
    inventory_lines = inventory.splitlines(1)
    correct_lines = correct_inventory.splitlines(1)
    # if the assertion fails, this diff will display
    diff = difflib.unified_diff(inventory_lines, correct_lines)
    print(''.join(diff))
    assert_equal(inventory, correct_inventory)
