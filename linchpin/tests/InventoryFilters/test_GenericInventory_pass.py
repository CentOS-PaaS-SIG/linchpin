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
def test_get_host_ips():
    """
    """
    ips = filter.get_host_ips(res_output)
    expected_hosts = ['aws', 'openstack', 'dummy', 'gcloud', 'beaker',
                      'libvirt', 'duffy', 'ovirt']
    assert_equal(set(ips), set(expected_hosts))
   
@with_setup(setup_generic_inventory_filter)
def test_get_hosts_by_count():
    """
    """
    host_dict = dict()
    host_dict['one'] = 'foo'
    host_dict['two'] = 'bar'
    expected_hosts = ['foo', 'bar']

    hosts = filter.get_hosts_by_count(host_dict, 0, ['one', 'two'])
    assert_equal(len(hosts), 0)
    hosts = filter.get_hosts_by_count(host_dict, 2, ['one', 'two'])
    assert_equal(len(hosts), 2)
    assert_equal(set(hosts), set(expected_hosts))


@with_setup(setup_generic_inventory_filter)
@with_setup(setup_generic_topology)
@with_setup(setup_generic_layout)
def test_get_inventory():
    """
    """
    inventory = filter.get_inventory(res_output, layout, topology)
    assert_true(inventory)