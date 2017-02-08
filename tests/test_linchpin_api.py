import os
import sys
import pdb
import shutil
from linchpin_api.v1.api import LinchpinAPI
from mockdata import inventory_mock as im
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from nose import with_setup


class TestLinchPinAPI(object):

    @classmethod
    def setup(self):
        """This method is run once before _each_ test method is executed"""
        pass

    @classmethod
    def teardown(self):
        """This method is run once for each class _after_ all tests are run"""
        pass

    def test_object_create(self):
        lp = LinchpinAPI()
        assert_equal(isinstance(lp, LinchpinAPI), True)

    def test_get_config_path(self):
        lp = LinchpinAPI()
        config_path = lp.get_config_path().split("/")[-1]
        assert_equal("linchpin_config.yml", config_path)

    def test_get_config(self):
        lp = LinchpinAPI()
        cfg = lp.get_config()
        keys = ['inventory_layouts_path',
                'inventory_outputs_path',
                'no_output',
                'async_timeout',
                'check_mode',
                'inventory_playbooks',
                'inventory_types',
                'outputfolder_path',
                'async',
                'keystore_path',
                'inventoryfolder_path',
                'schema']
        assert_equal(cfg.keys(), keys)

    @raises(TypeError)
    def test_get_evars_without_pf(self):
        lp = LinchpinAPI()
        evars = lp.get_evars()

    def test_get_evars(self):
        lp = LinchpinAPI()
        pf = im.get_mock_pf()
        lp.get_evars(pf)

    @raises(TypeError)
    def test_lp_list_without_params(self):
        lp = LinchpinAPI()
        lp = lp.lp_list()

    def test_lp_topo_list_without_params(self):
        lp = LinchpinAPI()
        lp = lp.lp_topo_list()
        assert_equal(isinstance(lp, list), True)
    
    @raises(Exception)
    def test_lp_topo_list_with_wrong_upstream(self):
        lp = LinchpinAPI()
        upstream = "www.example.com"
        lp = lp.lp_topo_list(upstream)
    
    def test_lp_layout_list_without_params(self):
        lp = LinchpinAPI()
        lp = lp.lp_layout_list()
        assert_equal(isinstance(lp, list), True)

    @raises(Exception)
    def test_lp_layout_list_with_wrong_upstream(self):
        lp = LinchpinAPI()
        upstream = "www.example.com"
        lp = lp.lp_alyout_list(upstream)
    
    @raises(TypeError)
    def test_lp_topo_get_without_params(self):
        lp = LinchpinAPI()
        lp = lp.lp_topo_get()

    @raises(IOError)
    def test_lp_topo_get_with_wrong_input_topo(self):
        lp = LinchpinAPI()
        topo = "thisdoesnotexists"
        lp = lp.lp_topo_get(topo)

    @raises(Exception)
    def test_lp_topo_get_with_wrong_upstream(self):
        lp = LinchpinAPI()
        topo = "thisdoesnotexists"
        upstream = "www.example.com"
        lp = lp.lp_topo_get(topo, upstream)

    @raises(TypeError)
    def test_lp_layout_get_without_params(self):
        lp = LinchpinAPI()
        lp = lp.lp_topo_get()

    def test_lp_drop(self):
        """
        test not implemented as there is no linchpin_api for rise
        """

    def test_lp_drop_with_target(self):
        """
        test not implemented as there is no linchpin_api for rise
        """
        pass

    def test_lp_rise(self):
        """
        test not implemented as there is no linchpin_api for rise
        """
        pass

    def test_lp_rise_with_target(self):
        """
        test not implemented as there is no linchpin_api for rise
        """
        pass

    @raises(TypeError)
    def test_lp_validate_topology_without_params(self):
        lp = LinchpinAPI()
        lp = lp.lp_validate()

    def test_lp_validate_topology(self):
        lp = LinchpinAPI()
        base_path = os.path.realpath(__file__)
        base_path = "/".join(base_path.split("/")[0:-2])
        topo = base_path+"/tests/mockdata/ex_all.yml"
        topo = os.path.abspath(topo)
        lp = lp.lp_validate(topo)
        assert_equal(lp, 0)

    def test_lp_invgen_with_params(self):
        lp = LinchpinAPI()
        of = im.get_mock_outputfile()
        lf = im.get_mock_layoutfile()
        io = os.getcwd()+"/testoutput.txt"
        lp.lp_invgen(of, lf, io, "generic")
        filegenerated = os.path.exists(io)
        if filegenerated:
            os.remove(io)
        assert_equal(filegenerated, True)

    @raises(TypeError)
    def test_lp_invgen_without_params(self):
        lp = LinchpinAPI()
        lp = lp.lp_invgen()
