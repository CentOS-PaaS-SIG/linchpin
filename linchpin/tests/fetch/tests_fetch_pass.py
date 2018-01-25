import os
import sys
import shutil

from nose.tools import assert_equal
from nose.tools import assert_list_equal
from nose.tools import with_setup

from linchpin.cli import LinchpinCli
from linchpin.cli.context import LinchpinCliContext
from linchpin.tests.mockdata.contextdata import ContextData


def test_context_create():

    lpc = LinchpinCliContext()
    assert_equal(isinstance(lpc, LinchpinCliContext), True)


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
    # cd.load_config_data(provider)
    cd.load_config_data()
    cd.create_config()
    config_path = cd.get_temp_filename()
    config_data = cd.cfg_data
    cd.write_config_file(config_path)


def setup_lp_fetch_env():
    global lpc
    global lpcli

    global target
    global pinfile
    global mockpath

    base_path = '{0}'.format(os.path.dirname(
        os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))

    setup_load_config()

    pinfile = 'PinFile'
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    lpc = LinchpinCliContext()
    lpc.load_config(lpconfig=config_path)
    lpc.load_global_evars()
    lpc.setup_logging()
    lpc.workspace = '/tmp/workspace/'
    mockpath = os.path.realpath(mock_path)

    if not os.path.exists(lpc.workspace):
        os.mkdir(lpc.workspace)

    lpcli = LinchpinCli(lpc)


@with_setup(setup_lp_fetch_env)
def test_fetch_local():

    src_path = os.path.join(mockpath, 'fetch/ws1')
    src_uri = 'file://{0}'.format(src_path)
    lpcli.lp_fetch(src_uri, root=None, fetch_type='workspace')

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
    lpcli.lp_fetch(src_url, root='ws1', fetch_type='topologies')

    src_list = ['topologies']
    dest_list = os.listdir(lpc.workspace)

    shutil.rmtree(lpc.workspace)
    shutil.rmtree(os.path.join(os.path.expanduser('~'), '.cache/linchpin/'))

    assert_list_equal(src_list, dest_list)


@with_setup(setup_lp_fetch_env)
def test_fetch_cache():

    src_url = 'https://github.com/agharibi/SampleLinchpinDirectory.git'
    lpcli.lp_fetch(src_url, root='ws1', fetch_type='topologies')

    cache_path = os.path.join(os.path.expanduser('~'), '.cache/linchpin/git')

    cache_dir_list = os.listdir(cache_path)
    shutil.rmtree(lpc.workspace)
    shutil.rmtree(os.path.join(os.path.expanduser('~'), '.cache/linchpin/'))

    assert_equal(1, len(cache_dir_list))


def main():

    setup_load_config()


if __name__ == '__main__':
    sys.exit(main())
