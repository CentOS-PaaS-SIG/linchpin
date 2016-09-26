import os
import sys
import json
import pdb
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from nose import with_setup 
from collections import namedtuple
filepath = os.path.realpath(__file__)
filepath = "/".join(filepath.split("/")[0:-2])
sys.path.append(filepath)
from InventoryFilters import AWSInventory
from InventoryFilters import OpenstackInventory
from InventoryFilters import GCloudInventory
from InventoryFilters import GenericInventory


class TestLinchPinInventoryFilters(object):
    @classmethod
    def setup(self):
        """This method is run once before _each_ test method is executed"""
        self.test_input = json.loads(open("mockdata/test_input.json","r").read())
        self.test_layout = json.loads(open("mockdata/test_layout.json","r").read())

    @classmethod
    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    @with_setup(setup)
    def test_filter_aws_get_host_ips(self):
        inv = AWSInventory.AWSInventory()
        host_ips = inv.get_host_ips(self.test_input)
        output = (type(host_ips) == list) and (len(host_ips) == 3)
        assert_equal(output, True)
    
    @with_setup(setup)
    def test_filter_os_get_host_ips(self):
        inv = OpenstackInventory.OpenstackInventory()
        host_ips = inv.get_host_ips(self.test_input)
        output = (type(host_ips) == list) and (len(host_ips) == 3)
        assert_equal(output, True)

    @with_setup(setup)
    def test_filter_gcloud_get_host_ips(self):
        inv = GCloudInventory.GCloudInventory()
        host_ips = inv.get_host_ips(self.test_input)
        output = (type(host_ips) == list) and (len(host_ips) == 3)
        assert_equal(output, True)
    
    @with_setup(setup)
    def test_filter_duffy_get_host_ips(self):
        pass


    @with_setup(setup)
    def test_filter_generic_get_host_ips(self):
        inv = GenericInventory.GenericInventory()
        host_ips = inv.get_host_ips(self.test_input)
        output = (len(host_ips.keys()) == 3) and (sum(len(v) for v in host_ips.itervalues()) == 9)
        assert_equal(output, True)

    @with_setup(setup)
    def test_filter_aws_get_inventory(self):
        inv = AWSInventory.AWSInventory()
        pass

    @with_setup(setup)
    def test_filter_os_get_inventory(self):
        inv = OpenstackInventory.OpenstackInventory()
        pass

    @with_setup(setup)
    def test_filter_gcloud_get_inventory(self):
        inv = GCloudInventory.GCloudInventory()
        pass

    @with_setup(setup)
    def test_filter_duffy_get_inventory(self):
        pass

    @with_setup(setup)
    def test_filter_generic_get_inventory(self):
        inv = GenericInventory.GenericInventory()
        pass
