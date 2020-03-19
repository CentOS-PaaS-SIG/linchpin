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
def test_cli_create():

    lpctx = LinchpinCliContext()
    lpctx.load_config()
    lpctx.load_global_evars()
    lpc = LinchpinCli(lpctx)

    assert_equal(isinstance(lpc, LinchpinCli), True)


@with_setup(setup_lp_cli)
def test_pinfile():
    pf = {}
    pf['foo'] = 'bar'

    # set the pinfile
    lpc.pinfile = pf

    # get the pinfile and verify that the data is correct
    data = lpc.pinfile

    assert_dict_equal(pf, data)


@with_setup(setup_lp_cli)
def test_pf_data():
    pf_data = {}
    pf_data['foo'] = 'bar'

    # set the pinfile
    lpc.pf_data = pf_data

    # get the pinfile and verify that the data is correct
    data = lpc.pf_data

    assert_dict_equal(pf_data, data)


@with_setup(setup_lp_cli)
def test_workspace():
    workspace = '/tmp/workspace'

    # set the pinfile
    lpc.workspace = workspace

    # get the pinfile and verify that the data is correct
    ws = lpc.workspace

    assert_equal(workspace, ws)


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

    # test that template leaves things that do not need to be templated
    template = lpc._render_template(layout_data, '{}')
    diff = [i1 for i1, i2 in zip(six.iteritems(layout_data), six.iteritems(template)) if i1 != i2]
    assert_false(diff)

    
    layout = 'template-inventory.yml'
    layout_file = open(mock_path+'/'+layout, 'r')
    layout_data = lpc.parser.parse_json_yaml(layout_file.read())
    layout_file.close()
    data = '{"executor_name": "lp_exec"}'
    template = lpc._render_template(layout_data, data)
    # test that template properly renders variables
    expected_hosts = ['lp_exec-master', 'lp_exec-node']
    hosts = set(template['inventory_layout']['hosts'])
    assert_equal(set(expected_hosts), hosts)
    # test that template turns variables without values into empty strings
    routehost = template['inventory_layout']['host_groups']['OSEv3']['vars']\
                ['openshift_hosted_registry_routehost']
    assert_equal(routehost, 'registry.cloudapps.')

    # test that returning no data will return the template
    template = {"one": "{{ two }}"}
    parsed = lpc._render_template(layout_data, None)


@with_setup(setup_lp_api)
def test_get_evar_item():

    test_evars = {'ekey2': 'evalue2'}
    for k, v in test_evars.items():
        lpa.set_evar(k, v)

    assert_equal(lpa.get_evar(key='ekey2'), test_evars.get('ekey2'))


@with_setup(setup_lp_cli)
def test_get_pinfile_path():
    try:
        lpc._get_pinfile_path()
    except LinchpinError as e:
        assert(e.contains('Please check that it exists and try again'))
    
    lpc.pinfile = 'PinFile.test'
    assert(lpc._get_pinfile_path(exists=False).endswith('PinFile.test'))   

    lpc.workspace = '/tmp'
    assert_equal(lpc._get_pinfile_path(exists=False),
                 '/tmp/PinFile.test')  


@with_setup(setup_lp_cli)
def test_get_data_path():
    # test the case in which the data is a string that doesn't start with '@' or
    # is none
    lpc.pf_data = None
    data_path = lpc._get_data_path()
    assert_equal(data_path, None)
    lpc.pf_data = '{}'
    data_path = lpc._get_data_path()
    assert_equal(data_path, None)

    # test the case in which the file is a full path
    lpc.pf_data = '@/tmp'
    data_path = lpc._get_data_path()
    assert_equal('/tmp', data_path)

    # test the case in which the file is not a full path and the workspace
    # is prepended
    lpc.pf_data = '@linchpin'
    data_path = lpc._get_data_path()
    assert(data_path.endswith('linchpin'))


@with_setup(setup_lp_cli)
def test_execute_action():
    ret_data = lpc._execute_action('up')
    assert_equal(ret_data[0], 0)
    run_id = list(ret_data[1])[0]
    tx_id = list(ret_data[1][run_id]['summary_data']['dummy'])[0]
    #lpc.pf_data = 'linchpin/tests/mockdata/templates/template-inventory.yml'
    ret_code = lpc._execute_action('up', run_id=run_id)[0]
    assert_equal(ret_code, 0)

    # test with use_pinfile == False
    lpc.ctx.set_cfg("lp", "use_rundb_for_actions", 'True')
    ret_code = lpc._execute_action('up', tx_id=tx_id)[0]
    # if we can get provision data into the rundb correctly we can make sure
    # this is 0 and increase test coverage as well
    assert_equal(ret_code, 99)


@with_setup(setup_lp_cli)
def test_find_include():
    lpc.workspace = os.path.realpath('linchpin/tests/mockdata/dummy')
    path = lpc.find_include('dummy-cluster.yml')
    assert(path.endswith('mockdata/dummy/topologies/dummy-cluster.yml'))

    path = lpc.find_include('dummy-layout.yml', ftype='layout')
    assert(path.endswith('mockdata/dummy/layouts/dummy-layout.yml'))

    path = lpc.find_include('dummy-hooks.yml', ftype='hooks')
    assert(path.endswith('mockdata/dummy/hooks/dummy-hooks.yml'))


@with_setup(setup_lp_cli)
def test_make_layout_integers():
    pf_w_path = lpc._get_pinfile_path()
    pf = lpc.parser.process(pf_w_path, data=None)
    provision_data = lpc._build(pf, pf_data=None)
    layout = provision_data['dummy']['layout']
    data = lpc._make_layout_integers(layout)
    field = data['inventory_layout']['hosts']['example-node']['count']
    assert_equal(type(field), int)

    # make count a string and try again
    provision_data = lpc._build(pf, pf_data=None)
    layout = provision_data['dummy']['layout']
    strfield = layout['inventory_layout']['hosts']['example-node']['count']
    strfield = str(strfield)
    data = lpc._make_layout_integers(layout)
    field = data['inventory_layout']['hosts']['example-node']['count']
    assert_equal(type(field), int)


@with_setup(setup_lp_cli)
def test_build():
    pf_w_path = lpc._get_pinfile_path()
    pf = lpc.parser.process(pf_w_path, data=None)
    provision_data = lpc._build(pf)

    # get topology file and compare it to provision_data['topology']
    topology_file = "{0}/topologies/dummy-cluster.yml".format(lpc.workspace)
    with open(topology_file, 'r') as topology_yaml:
        topology = yaml.load(topology_yaml,
                             Loader=yamlordereddictloader.Loader)
        assert_dict_equal(topology, provision_data['dummy']['topology'])
    # get layout file and compare it to provision_data['layout']
    layout_file = "{0}/layouts/dummy-layout.yml".format(lpc.workspace)
    with open(layout_file, 'r') as layout_yaml:
        layout = yaml.load(layout_yaml, Loader=yamlordereddictloader.Loader)
        assert_dict_equal(layout, provision_data['dummy']['layout'])
    # get hooks file and compare it to provision_data['hooks']
    hooks_file = "{0}/hooks/dummy-hooks.yml".format(lpc.workspace)
    with open(hooks_file, 'r') as hooks_yaml:
        hooks = yaml.load(hooks_yaml, Loader=yamlordereddictloader.Loader)
        assert_dict_equal(hooks, provision_data['dummy']['hooks'])


@with_setup(setup_lp_cli)
def test_execute():
    # get provision data from PinFile
    pf_w_path = lpc._get_pinfile_path()
    pf = lpc.parser.process(pf_w_path, data=None)
    provision_data = lpc._build(pf, pf_data=None)
    # test with no targets
    ret_code = lpc._execute(provision_data, [])[0]
    assert_equal(ret_code, 0)

    # test with a specific target
    # rebuild because lpc._execute() or one of its sub-functions modifies
    # the provisioning data
    provision_data = lpc._build(pf, pf_data=None)
    ret_code = lpc._execute(provision_data, ['dummy'])[0]
    assert_equal(ret_code, 0)


@with_setup(setup_lp_cli)
def test_lp_fetch():
    # test where dest_ws == '.'
    # test where dest_ws != '.'
    # test where the path does not exist
    src = 'https://github.com/CentOS-PaaS-SIG/linchpin'
    root = 'linchpin/tests/mockdata/dummy'
    fetch_type = 'topologies'
    fetch_ref = 'develop'
    dest_ws = '/tmp/test-lp-fetch-{0}'.format(time.time())
    os.mkdir(dest_ws)

    # test where destination workspace != workdir
    
    lpc.lp_fetch(src,
                 root=root,
                 fetch_type=fetch_type,
                 fetch_ref=fetch_ref,
                 dest_ws=dest_ws)
    # check that the 'dummy' folder exists in dest_ws and that the only
    # sub-folder is 'topologies'
    cloned_ws = '{0}/dummy'.format(dest_ws)
    assert(os.path.exists(cloned_ws))
    children = os.listdir(cloned_ws)
    assert_equal(len(children), 1)
    assert_equal(children[0], 'topologies')
    shutil.rmtree(dest_ws)

    # test where destination workspace == None  
    os.mkdir(dest_ws)
    lpc.workspace = dest_ws
    lpc.lp_fetch(src,
                 root=root,
                 fetch_type='workspace',
                 fetch_protocol='FetchGit',
                 fetch_ref=fetch_ref,
                 dest_ws=None,
                 nocache=True)
    # check that the 'dummy' folder exists in cwd and that it contains the
    # sub-folders 'topologies' 'layouts' and 'hooks'
    assert(os.path.exists(cloned_ws))
    children = os.listdir(cloned_ws)
    assert('topologies' in children)
    assert('layouts' in children)
    assert('linchpin.conf' in children)
    assert('PinFile' in children)

    # clean up
    shutil.rmtree(dest_ws)


@with_setup(setup_lp_cli)
def test_lp_init():
    ws_path = '/tmp/lp-{0}'.format(time.time())
    lpc.pinfile = pinfile
    lpc.workspace = ws_path
    providers=['dummy']

    lpc.lp_init(providers=providers)


@with_setup(setup_lp_cli)
def test_lp_up_use_api():
    # disable hooks, which are causing the test to hang
    lpc.ctx.set_cfg("hook_flags", "no_hooks", True)

    run_data = lpc.lp_up()
    return_code = run_data[0]
    rundb_id = list(run_data[1])[0]
    assert_equal(return_code, 0)

    # TODO: make these lines work
    # If a run_id is provided, the run_id for the run should be the same so
    # that the run can be idempotent, but this doesn't work at the moment
    # run_data2 = lpc.lp_up(run_id=str(rundb_id))
    # assert_dict_equal(run_data[1], run_data2[1])


@with_setup(setup_lp_cli)
def test_lp_up_use_shell():
    # disable hooks, which are causing the test to hang
    lpc.ctx.set_cfg("hook_flags", "no_hooks", True)
    lpc.ctx.set_cfg("ansible", "use_shell", True)

    run_data = lpc.lp_up()
    return_code = run_data[0]
    rundb_id = list(run_data[1])[0]
    assert_equal(return_code, 0)

    # TODO: make these lines work
    # If a run_id is provided, the run_id for the run should be the same so
    # that the run can be idempotent, but this doesn't work at the moment
    # run_data2 = lpc.lp_up(run_id=str(rundb_id))
    # assert_dict_equal(run_data[1], run_data2[1])


@with_setup(setup_lp_cli)
def test_lp_validate():
    rc = lpc.lp_validate()[0]
    assert_equal(rc, 0)


@with_setup(setup_lp_cli)
def test_lp_setup():
    lpc.ctx.set_evar("use_venv", True)
    providers = ['docs', 'test']
    output = lpc.lp_setup(providers=providers)
    assert_equal(output[0], 0)


@with_setup(setup_lp_cli)
def test_lp_destroy():
    # disable hooks, which are causing the test to hang
    lpc.ctx.set_cfg("hook_flags", "no_hooks", True)
    lpc.lp_up()
    outputs = lpc.lp_destroy()
    return_code = outputs[0]
    assert_equal(return_code, 0)


@with_setup(setup_lp_cli)
def test_write_to_inventory():
    lpc._write_to_inventory()
    
    # test run with inventory path set
    inv_path = '/tmp/inventory-{0}'.format(time.time())
    lpc._write_to_inventory(inv_path=inv_path)


@with_setup(setup_lp_cli)
def test_write_distilled_context():
    # TODO: flesh this out
    lpc._write_distilled_context({})


def main():
    pass


if __name__ == '__main__':
    sys.exit(main())
