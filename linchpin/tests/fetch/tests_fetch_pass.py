import os
import sys
import time
import shutil
import tempfile

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

    lpc = LinchpinCliContext()
    lpc.load_config(lpconfig=config_path)
    lpc.load_global_evars()
    lpc.setup_logging()

    lpc.workspace = tempfile.mkdtemp(prefix='fetch_')
    print('workspace: {0}'.format(lpc.workspace))

    lpcli = LinchpinCli(lpc)


@with_setup(setup_lp_fetch_env)
def test_fetch_git():

    shutil.rmtree(lpc.workspace)
    os.makedirs(lpc.workspace)
    os.chdir(lpc.workspace)
    src_url = 'git://github.com/herlo/lp_test_workspaces'
    root_dir = 'os-server-addl-vols'

    lpcli.lp_fetch(src_url, root=root_dir)

    chk_dir = '{0}/{1}/'.format(lpc.workspace, root_dir)
    assert(os.path.exists('{0}/PinFile'.format(chk_dir)))


@with_setup(setup_lp_fetch_env)
def test_fetch_http():

    shutil.rmtree(lpc.workspace)
    os.makedirs(lpc.workspace)
    os.chdir(lpc.workspace)
    src_url = 'https://herlo.fedorapeople.org'
    root_dir = 'simple'

    lpcli.lp_fetch(src_url, root='lp_ws/{0}'.format(root_dir),
                   fetch_protocol='FetchHttp')

    chk_dir = '{0}/{1}/'.format(lpc.workspace, root_dir)
    assert(os.path.exists('{0}/PinFile'.format(chk_dir)))


def main():

    setup_load_config()


if __name__ == '__main__':
    sys.exit(main())
