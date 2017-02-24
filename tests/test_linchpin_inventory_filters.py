import os
import sys
import json
import StringIO
import io
import pdb
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
try:
    import mock
except ImportError:
    from unittest import mock
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from nose import with_setup
from collections import namedtuple
from InventoryFilters import AWSInventory
from InventoryFilters import OpenstackInventory
from InventoryFilters import GCloudInventory
from InventoryFilters import GenericInventory
from linchpin_utils import inventory_utils
from mockdata import inventory_mock as im
from camel import Camel
filepath = os.path.realpath(__file__)
filepath = "/".join(filepath.split("/")[0:-2])
sys.path.append(filepath)


class TestLinchPinInventoryFilters(object):

    def setup(self):
        """This method is run once before _each_ test method is executed"""
        self.test_input = im.get_mock_topo_output()
        self.test_layout = im.get_mock_layout()

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
        noofhosts = len(host_ips.keys())
        hostips = sum(len(v) for v in host_ips.itervalues())
        output = (noofhosts == 6) and (hostips == 9)
        assert_equal(output, True)

    @with_setup(setup)
    def test_filter_aws_get_inventory(self):
        inv = AWSInventory.AWSInventory()
        output = inv.get_inventory(self.test_input, self.test_layout)
        sections = inventory_utils.get_sections(output)
        assert_equal(len(sections), 7)

    @with_setup(setup)
    def test_filter_os_get_inventory(self):
        inv = OpenstackInventory.OpenstackInventory()
        output = inv.get_inventory(self.test_input, self.test_layout)
        sections = inventory_utils.get_sections(output)
        assert_equal(len(sections), 7)

    @with_setup(setup)
    def test_filter_gcloud_get_inventory(self):
        inv = GCloudInventory.GCloudInventory()
        output = inv.get_inventory(self.test_input, self.test_layout)
        sections = inventory_utils.get_sections(output)
        assert_equal(len(sections), 7)

    @with_setup(setup)
    def test_filter_duffy_get_inventory(self):
        pass

    @with_setup(setup)
    def test_filter_generic_get_inventory(self):
        inv = GenericInventory.GenericInventory()
        layout_data = Camel().dump(self.test_layout)
        output = inv.get_inventory(self.test_input, layout_data)
        sections = inventory_utils.get_sections(output)
        assert_equal(len(sections), 7)
