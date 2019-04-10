import os
import sys

from nose.tools import assert_equal
from nose.tools import assert_false
from nose.tools import assert_dict_equal
from nose.tools import assert_dict_contains_subset
from nose.tools import with_setup

from linchpin import LinchpinAPI
from linchpin.cli import LinchpinCli
from linchpin.cli.context import LinchpinCliContext
from linchpin.tests.mockdata.contextdata import ContextData


def test_cli_create():

    lpctx = LinchpinCliContext()
    lpctx.load_config()
    lpctx.load_global_evars()
    lpc = LinchpinCli(lpctx)

    assert_equal(isinstance(lpc, LinchpinCli), True)

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

    lpc = LinchpinCliContext()
    lpc.load_config(lpconfig=config_path)
    lpc.load_global_evars()
    lpc.setup_logging()
    lpc.workspace = os.path.realpath(mock_path)

    lpa = LinchpinAPI(lpc)


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

    lpc = LinchpinCli(lpctx)


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


@with_setup(setup_lp_cli)
def test_render_template():
    # load data as ordereddict
    provider = 'layouts'
    base_path = '{0}'.format(os.path.dirname(
    os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)
    layout = 'render_order.yml'
    layout_file = open(mock_path+'/'+layout, 'r')
    layout_data = lpc.parser.parse_json_yaml(layout_file.read())
    layout_file.close()

    # render template
    template = lpc._render_template(layout_data, '{}')

    # compare two ordered dicts
    diff = [i1 for i1, i2 in zip(layout_data.iteritems(), template.iteritems()) if i1 != i2]
    assert_false(diff)


@with_setup(setup_lp_api)
def test_get_evar_item():

    test_evars = {'ekey2': 'evalue2'}
    for k, v in test_evars.items():
        lpa.set_evar(k, v)

    assert_equal(lpa.get_evar(key='ekey2'), test_evars.get('ekey2'))


def main():
    pass


if __name__ == '__main__':
    sys.exit(main())
