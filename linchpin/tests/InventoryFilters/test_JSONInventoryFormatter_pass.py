#!/user/bin/env python

import os
import json

from nose.tools import *
from six import iteritems

from linchpin.InventoryFilters import JSONInventoryFormatter

def setup_json_inventory_formatter():
    global formatter
    global inv

    formatter = JSONInventoryFormatter.JSONInventoryFormatter()
    subdir = 'layouts'
    base_path = '{0}'.format(os.path.dirname(
        os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', subdir)
    
    template = 'parsed-layout.json'
    template_file = open(mock_path+'/'+template)
    inv = json.load(template_file)


@with_setup(setup_json_inventory_formatter)
def test_add_sections():
    """ 
    should add a list of sections to the config, as well as "all"
    """
    section_list = ['foo', 'bar']

    formatter.add_sections(section_list)
    sections = formatter.config
    assert_equal(set(sections), set(['foo','bar','all']))


@with_setup(setup_json_inventory_formatter)
def test_set_children():
    """
    Should set the children of each inventory host group in the config
    """
    empty_inv = dict()
    formatter.set_children(empty_inv)

    formatter.set_children(inv)

    host_group='OSEv3'
    # if one if these does not exist, a NoOptionError will be thrown
    for child in inv['host_groups'][host_group]['children']:
        formatter.config.get('{0}:children'.format(host_group), child)


@with_setup(setup_json_inventory_formatter)
def test_set_vars():
    """
    Should add the vars in each host_group to the config
    """
    empty_inv = dict()
    formatter.set_vars(empty_inv)

    formatter.add_sections(inv['host_groups'].keys())
    formatter.set_vars(inv)

    host_group='OSEv3'
    vars = formatter.config[host_group]['vars']
    for key, val in iteritems(inv['host_groups'][host_group]['vars']):
        assert_equal(val, vars[key])


@with_setup(setup_json_inventory_formatter)
def test_add_ips_to_groups():
    """
    """
    inven_hosts = inv['hosts']
    formatter.add_sections(inv['host_groups'].keys())
    formatter.add_ips_to_groups(inven_hosts, inv)
 

@with_setup(setup_json_inventory_formatter)
def test_add_common_vars():
    """
    """
    host_groups = inv['host_groups'].keys()
    formatter.add_sections(host_groups)
    formatter.set_vars(inv)
    formatter.add_ips_to_groups(host_groups, inv)
    formatter.add_common_vars(host_groups, inv)


@with_setup(setup_json_inventory_formatter)
def test_generate_inventory():
    """
    """
    inv_json = formatter.generate_inventory()
    # if the json is not valid, this will throw a ValueError and the test
    # will fail
    data = json.loads(inv_json)#!/user/bin/env python