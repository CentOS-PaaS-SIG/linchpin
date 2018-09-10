#!/usr/bin/env python

# flake8: noqa

import os
import json
import yaml

from nose.tools import *

import logging
from unittest import TestCase

from linchpin.InventoryFilters import AWSInventory

def setup_aws_inventory():
    global filter
    global topo

    filter = AWSInventory.AWSInventory()
    
    provider = 'general'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    topology = 'topo.json'
    topo_file = open(mock_path+'/'+topology)
    topo = json.load(topo_file)
    topo_file.close()

def setup_aws_config():
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

def setup_aws_layout():
    global layout

    provider = 'layouts'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    template = 'parsed-layout.json'
    template_file = open(mock_path+'/'+template)
    layout = json.load(template_file)

@with_setup(setup_aws_inventory)
@with_setup(setup_aws_config)
def test_get_host_data():
    """
    """
    host_data = filter.get_host_data(topo, config)
    expected_vars = ['__IP__']
    for host in host_data:
        assert_equal(set(host_data[host].keys()), set(expected_vars))

@with_setup(setup_aws_inventory)
@with_setup(setup_aws_config)
def test_get_host_ips():
    """
    """
    host_data = filter.get_host_data(topo, config)
    ips = filter.get_host_ips(host_data)
    expected_hosts = ['54.123.12.15.compute-1.amazonaws.com', '121.22.32.224',
                      '119.120.37.31']
    assert_equal(set(host_data.keys()), set(expected_hosts))

@with_setup(setup_aws_inventory)
@with_setup(setup_aws_config)
@with_setup(setup_aws_layout)
def test_get_inventory():
    """
    """
    empty_topo = dict()
    empty_topo['aws_ec2_res'] = []
    inventory = filter.get_inventory(empty_topo, layout, config)
    assert_false(inventory)
    inventory = filter.get_inventory(topo, layout, config)
    assert_true(inventory)