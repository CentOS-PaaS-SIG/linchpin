#!/usr/bin/env python

# flake8: noqa

import os
import json

from nose.tools import *
from six import iteritems

import logging
from unittest import TestCase

from linchpin.InventoryFilters import GenericInventory

def setup_inventory_filter():
    global filter
    global inv

    filter = GenericInventory.GenericInventory()
    subdir = 'layouts'
    base_path = '{0}'.format(os.path.dirname(
        os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', subdir)

    template = 'parsed-layout.json'
    template_file = open(mock_path+'/'+template)
    inv = json.load(template_file)

@with_setup(setup_inventory_filter)
def test_get_layout_hosts():
    """
    Should return the number of hosts in an inventory file.
    """
    hosts = filter.get_layout_hosts(inv)
    assert_equal(hosts, 3)

@with_setup(setup_inventory_filter)
def test_get_layout_host_groups():
    """
    Should return a list of the host_groups in an inventory file.
    """
    
    host_groups = filter.get_layout_host_groups(inv)
    # casting to sets ensures that only the elements (not order) are considered
    assert_equal(set(host_groups),
        set(['masters', 'etcd', 'nodes', 'nfs', 'glusterfs']))

@with_setup(setup_inventory_filter)
def test_add_sections():
    """
    should add a list of sections to the config, as well as "all"
    """
    section_list = ['foo', 'bar']

    filter.add_sections(section_list)
    sections = filter.config.sections()
    assert_equal(set(sections), set(['foo','bar','all']))

@with_setup(setup_inventory_filter)
def test_set_children():
    """
    Should set the children of each inventory host group in the config
    """
    empty_inv = dict()
    filter.set_children(empty_inv)

    filter.set_children(inv)

    host_group='OSEv3'
    # if one if these does not exist, a NoOptionError will be thrown
    for child in inv['host_groups'][host_group]['children']:
        filter.config.get('{0}:children'.format(host_group), child)

@with_setup(setup_inventory_filter)
def test_set_vars():
    """
    Should add the vars in each host_group to the config
    """
    empty_inv = dict()
    filter.set_vars(empty_inv)

    filter.set_vars(inv)

    host_group='OSEv3'
    for key, val in iteritems(inv['host_groups'][host_group]['vars']):
        var = filter.config.get("{0}:vars".format(host_group), key)
        assert_equal(var, str(val))

@with_setup(setup_inventory_filter)
def test_add_ips_to_groups():
    """
    I don't know what this is
    """
    inven_hosts = inv['hosts']
    filter.add_ips_to_groups(inven_hosts, inv)

@with_setup(setup_inventory_filter)
def test_add_common_vars():
    """
    I don't know what this is
    """
    host_groups = inv['host_groups'].keys()
    filter.add_sections(host_groups)
    filter.set_vars(inv)
    filter.add_ips_to_groups(host_groups, inv)
    filter.add_common_vars(host_groups, inv)