#!/usr/bin/env python

# flake8: noqa

from __future__ import print_function
from __future__ import absolute_import
import os
import json
import yaml
import json
import difflib

from configparser import ConfigParser

from nose.tools import *

from linchpin.context import LinchpinContext
from linchpin import LinchpinAPI
from linchpin.InventoryFilters import GenericInventory
from linchpin.tests.mockdata.contextdata import ContextData

def setup_generic_inventory_filter():
    global filter
    global res_output

    cd = ContextData()
    cd.load_config_data()
    config_path = cd.get_temp_filename()
    config_data = cd.cfg_data
    cd.write_config_file(config_path)
    lpc = LinchpinContext()
    lpc.load_config(search_path=[config_path])
    lpc.load_global_evars()
    lpc.setup_logging()

    lpa = LinchpinAPI(lpc)


    filter = GenericInventory.GenericInventory(pb_path=lpa.pb_path)

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
    topology = yaml.load(topo_file, Loader=yaml.FullLoader)['general-inventory']['topology']
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
    config = yaml.load(cfg_file, Loader=yaml.FullLoader)['general-inventory']['cfgs']
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
            assert_true('__IP__' in list(data[host].keys()))
            hosts.append(data[host]['__IP__'])
    expected_hosts = ['10.179.254.83', 'hp-dl380pgen8-02-vm-15.lab.bos.redhat.com', 'dummy-744068-0', 'dummy-744068-1', 'dummy-744068-2', '192.168.122.219', '172.16.100.11', '155.132.55.17', '11.50.197.1', '109.254.93.117', '180.20.194.96', '194.231.24.112', '171.109.242.199', 'test.example.com', '192.168.122.210']
    assert_equal(set(hosts), set(expected_hosts))


@with_setup(setup_generic_inventory_filter)
@with_setup(setup_generic_config)
def test_get_hosts_by_count():
    """
    """
    host_data = filter.get_host_data(res_output, config)
    expected_hosts = ['10.179.254.83', 'hp-dl380pgen8-02-vm-15.lab.bos.redhat.com', 'dummy-744068-0']
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
