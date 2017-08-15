import os
import shutil

from nose.tools import *

import logging
from unittest import TestCase

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser as ConfigParser

from linchpin.api import LinchpinAPI
from linchpin.api.context import LinchpinContext
from linchpin.tests.mockdata.contextdata import ContextData


def test_api_create():

    lpc = LinchpinContext()
    lpc.load_config()
    lpa = LinchpinAPI(lpc)

    assert_equal(isinstance(lpa, LinchpinAPI), True)


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
    #cd.load_config_data(provider)
    cd.load_new_config(provider)
    cd.parse_config()
    config_path = cd.get_temp_filename()
    config_data = cd.cfg_data
    cd.write_config_file(config_path)


def setup_lp_api():

    """
    Perform setup of LinchpinContext, lpc.load_config, and LinchPinAPI
    """

    global lpc
    global lpa

    global target
    global pinfile

    base_path = '{0}'.format(os.path.dirname(
        os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))

    setup_load_config()

    pinfile = 'PinFile'
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    lpc = LinchpinContext()
    lpc.load_config(lpconfig=config_path)
    lpc.load_global_evars()
    lpc.setup_logging()
    lpc.workspace = os.path.realpath(mock_path)

    lpa = LinchpinAPI(lpc)

def setup_lp_fetch_env():
    global lpc
    global lpa

    global target
    global pinfile
    global mockpath

    base_path = '{0}'.format(os.path.dirname(
        os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))

    setup_load_config()

    pinfile = 'PinFile'
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    lpc = LinchpinContext()
    lpc.load_config(lpconfig=config_path)
    lpc.load_global_evars()
    lpc.setup_logging()
    lpc.workspace = '/tmp/workspace/'
    mockpath = os.path.realpath(mock_path)

    if not os.path.exists(lpc.workspace):
        os.mkdir(lpc.workspace)

    lpa = LinchpinAPI(lpc)


@with_setup(setup_lp_api)
def test_config_extension():
    test_dict = {
                'alex': '/path/to/alex',
                'clint': '/path/to/clint', 
                'bob': '/path/to/bob'
            }
    assert_dict_equal(test_dict, lpa.ctx.cfgs['users'])

@with_setup(setup_lp_api)
def test_config_override():
    test_dict = {
                'credentials': 'True',
                'hooks': 'False',
                'inventories': 'True',
                'layouts': 'False',
                'resources': 'False'
            }
    assert_dict_equal(test_dict, lpa.ctx.cfgs['core_workspace_dirs'])

@with_setup(setup_lp_api)
def test_set_cfg():

    test_dict = {'key': 'value', 'key2': 'value2'}

    for k, v in test_dict.items():
        lpa.set_cfg('test', k, v)

    assert_dict_equal(test_dict, lpa.ctx.cfgs.get('test'))


@with_setup(setup_lp_api)
def test_get_cfg_section():

    lpa.set_cfg('test', 'key', 'value')
    lpa_dict = lpa.get_cfg('test')

    assert_dict_equal(lpa_dict, lpa.ctx.cfgs.get('test'))


@with_setup(setup_lp_api)
def test_get_cfg_item():

    lpa.set_cfg('test', 'key', 'value')
    lpa_value = lpa.get_cfg('test', 'key')

    test_dict = lpa.ctx.cfgs.get('test')
    test_value = test_dict.get('key')

    assert_equal(lpa_value, test_value)


@with_setup(setup_lp_api)
def test_set_evar():

    test_evars = {'ekey': 'evalue'}

    for k, v in test_evars.items():
        lpa.set_evar(k, v)
    lpa_evars = lpa.get_cfg('evars')

    assert_dict_contains_subset(test_evars, lpa_evars)


@with_setup(setup_lp_api)
def test_get_all_evars():

    test_evars = {'ekey1': 'evalue1', 'ekey2': 'evalue2'}
    for k, v in test_evars.items():
        lpa.set_evar(k, v)

    lpa_evars = lpa.get_evar()

    assert_dict_contains_subset(test_evars, lpa_evars)


@with_setup(setup_lp_api)
def test_get_evar_item():

    test_evars = {'ekey2': 'evalue2'}
    for k, v in test_evars.items():
        lpa.set_evar(k, v)

    assert_equal(lpa.get_evar(key='ekey2'), test_evars.get('ekey2'))


#def setup_lp_api():
#
#    """
#    Perform setup of LinchpinContext, lpc.load_config, and LinchPinAPI
#    """
#
#    global lpc
#    global lpa
#
#    lpc = LinchpinContext()
#    lpc.load_config()
#    lpa = LinchpinAPI(lpc)

@with_setup(setup_lp_api)
def test_run_playbook():

    pf_w_path = '{0}/{1}'.format(lpc.workspace, pinfile)
    return_code, results = lpa.run_playbook(pf_w_path, targets=[provider])

    for res in results[provider]:
        name = res._task.get_name()
        failed = False
        if res.is_failed():
            failed = True

    assert not failed

@with_setup(setup_lp_fetch_env)
def test_fetch_local():
    src_path = os.path.join(mockpath, 'fetch/ws1')
    src_uri = 'file://{0}'.format(src_path)
    lpa.lp_fetch(src_uri, 'workspace', None)

    src_list = os.listdir(src_path)
    dest_list = os.listdir(lpc.workspace)
    src_list.sort()
    dest_list.sort()
    shutil.rmtree(lpc.workspace)
    shutil.rmtree(os.path.join(os.path.expanduser('~'), '.cache/linchpin/'))
    assert_list_equal(src_list, dest_list)

@with_setup(setup_lp_fetch_env)
def test_fetch_git():
    src_url = 'https://github.com/agharibi/SampleLinchpinDirectory.git'
    lpa.lp_fetch(src_url, 'topologies', 'ws1')

    src_list = ['topologies']
    dest_list = os.listdir(lpc.workspace)

    shutil.rmtree(lpc.workspace)
    shutil.rmtree(os.path.join(os.path.expanduser('~'), '.cache/linchpin/'))

    assert_list_equal(src_list, dest_list)

@with_setup(setup_lp_fetch_env)
def test_fetch_cache():
    src_url = 'https://github.com/agharibi/SampleLinchpinDirectory.git'
    lpa.lp_fetch(src_url, 'topologies', 'ws1')
    lpa.lp_fetch(src_url, 'topologies', 'ws1')

    cache_path = os.path.join(os.path.expanduser('~'), '.cache/linchpin/git')

    cache_dir_list = os.listdir(cache_path)
    shutil.rmtree(lpc.workspace)
    shutil.rmtree(os.path.join(os.path.expanduser('~'), '.cache/linchpin/'))

    assert_equal(1, len(cache_dir_list))


def main():

    pass

if __name__ == '__main__':
    sys.exit(main())
