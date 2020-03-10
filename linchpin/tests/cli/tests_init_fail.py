from __future__ import absolute_import
import os
import sys
import time
import yaml
import yamlordereddictloader
import shutil

from nose.tools import assert_equal
from nose.tools import assert_false
from nose.tools import assert_dict_equal
from nose.tools import assert_raises
from nose.tools import assert_dict_contains_subset
from nose.tools import with_setup

from linchpin import LinchpinAPI
from linchpin.cli import LinchpinCli
from linchpin.cli.context import LinchpinCliContext
from linchpin.tests.mockdata.contextdata import ContextData
from linchpin.exceptions import LinchpinError
from linchpin.exceptions import TopologyError

import six
from six.moves import zip


# ------------------------------- #
#    Setup functions for tests    #
# ------------------------------- #
def setup_load_config():

    """
    Perform setup of ContextData() object, and run get_temp_filename()
    """

    global cd
    global provider
    global config_path
    global config_data

    provider = 'dummy'

    cd = ContextData()
    cd.load_config_data()
    cd.create_config()
    config_path = cd.get_temp_filename()
    config_data = cd.cfg_data
    cd.write_config_file(config_path)


def setup_lp_cli():

    """
    Perform setup of LinchpinContext, lpc.load_config, and LinchPinAPI
    """

    global lpctx
    global lpc

    global target
    global pinfile

    base_path = '{0}'.format(os.path.dirname(
        os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))

    setup_load_config()

    pinfile = 'PinFile'
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    lpctx = LinchpinCliContext()
    lpctx.load_config(lpconfig=config_path)
    lpctx.load_global_evars()
    lpctx.setup_logging()
    lpctx.workspace = os.path.realpath(mock_path)
    lpctx.pinfile = pinfile
    lpctx.pf_data = None
    lpctx.no_monitor = True
    lpctx.set_evar("no_monitor", True)
    lpctx.set_cfg("progress_bar", "no_progress", str(True))

    lpc = LinchpinCli(lpctx)
    lpc.disable_pbar = True
 


# ----------- #
#    Tests    #
# ----------- #
@with_setup(setup_lp_cli)
def test_get_data_path():
    # test the case in which the file is a full path that does not exist
    subdir = 'lp-test-get-data-path-{0}'.format(time.time())
    lpc.pf_data = '@/tmp/{0}'.format(subdir)
    assert_raises(TopologyError, lpc._get_data_path)
