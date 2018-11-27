#!/usr/bin/env python

# flake8: noqa

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

    provider = 'general'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    res_output = 'topo.json'
    res_file = open(mock_path+'/'+res_output)
    res_output = json.load(res_file)
    res_file.close()

def setup_generic_topology():
    global topology

    provider = 'dummy'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    topo = 'topologies/dummy-cluster.yml'
    topo_file = open(mock_path+'/'+topo)
    topology = yaml.load(topo_file)
    topo_file.close()

def setup_generic_config():
    global config

    provider = 'general'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    cfg = 'config.yml'
    cfg_file = open(mock_path+'/'+cfg)
    config = yaml.load(cfg_file)
    cfg_file.close()

def setup_generic_layout():
    global layout

    provider = 'layouts'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    template = 'parsed-layout.json'
    template_file = open(mock_path+'/'+template)
    layout = json.load(template_file)

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
    expected_providers = ['aws', 'openstack', 'dummy', 'gcloud', 'beaker',
                          'libvirt', 'duffy', 'ovirt']
    assert_equal(set(host_data.keys()), set(expected_providers))

    for provider in host_data:
        for host in host_data[provider]:
            if provider == 'dummy' or provider == 'duffy':
                continue
            assert_true('__IP__' in host_data[provider][host].keys())


@with_setup(setup_generic_inventory_filter)
def test_get_hosts_by_count():
    """
    """
    host_dict = dict()
    host_dict['openstack'] = {}
    host_dict['openstack']['os1'] = 'one'
    host_dict['libvirt'] = {}
    host_dict['libvirt']['l1'] = 'one'
    host_dict['libvirt']['l2'] = 'two'
    expected_hosts = ['os1', 'l1', 'l2']

    hosts = filter.get_hosts_by_count(host_dict, 0, ['openstack', 'libvirt'])
    assert_equal(len(hosts), 0)
    hosts = filter.get_hosts_by_count(host_dict, 3, ['openstack', 'libvirt'])
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
    res_output = res_output[res_output.keys()[0]]['targets'][0]['complex-inventory']['outputs']['resources']

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
    print ''.join(diff)
    assert_equal(inventory, correct_inventory)
