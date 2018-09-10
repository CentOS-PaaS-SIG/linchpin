#!/usr/bin/env python

# flake8: noqa

import os
import json
import yaml

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