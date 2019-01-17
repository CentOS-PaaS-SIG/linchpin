import os
import sys

from nose.tools import assert_equal
from nose.tools import assert_dict_equal
from nose.tools import assert_is_instance
from nose.tools import assert_dict_contains_subset
from nose.tools import with_setup

from linchpin import LinchpinAPI
from linchpin.utils.dataparser import DataParser
from linchpin.context import LinchpinContext
from linchpin.rundb import RunDB

from linchpin.tests.mockdata.contextdata import ContextData


def test_api_create():

    lpc = LinchpinContext()
    lpc.load_config()
    lpc.load_global_evars()
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
    global pf_data
    global target
    global provision_data

    setup_load_config()

    lpc = LinchpinContext()
    lpc.load_config(search_path=[config_path])
    lpc.load_global_evars()
    lpc.setup_logging()

    lpa = LinchpinAPI(lpc)

    pinfile = lpc.get_cfg('init', 'pinfile', default='PinFile')

    base_path = '{0}'.format(os.path.dirname(
        os.path.realpath(__file__))).rstrip('/')
    mock_path = '{0}/{1}/{2}'.format(base_path, 'mockdata', provider)

    if not lpa.workspace:
        lpa.workspace = mock_path

    lpa.set_evar('workspace', mock_path)

    pf_w_path = '{0}/PinFile'.format(mock_path, pinfile)

    parser = DataParser()
    pf_d = None
    pf_data = parser.process(pf_w_path)

    topo_folder = lpc.get_evar('topologies_folder')
    topo_file = pf_data[provider]["topology"]
    topo_path = '{0}/{1}/{2}'.format(mock_path, topo_folder, topo_file)
    with open(topo_path, 'r') as topo_stream:
        topology_data = parser.parse_json_yaml(topo_stream)
        provision_data = {provider: {'topology': topology_data}}


@with_setup(setup_lp_api)
def test_setup_rundb():

    rundb = lpa.setup_rundb()
    assert_is_instance(rundb, RunDB)


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
def test_set_cfg():

    test_dict = {'key': 'value', 'key2': 'value2'}

    for k, v in test_dict.items():
        lpa.set_cfg('test', k, v)

    assert_dict_equal(test_dict, lpa.ctx.cfgs.get('test'))


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


@with_setup(setup_lp_api)
def test_set_evar():

    test_evars = {'ekey': 'evalue'}

    for k, v in test_evars.items():
        lpa.set_evar(k, v)
    lpa_evars = lpa.get_cfg('evars')

    assert_dict_contains_subset(test_evars, lpa_evars)


@with_setup(setup_lp_api)
def test_set_hook_state():

    pass


@with_setup(setup_lp_api)
def test_bind_to_hook_state():

    pass



@with_setup(setup_lp_api)
def test_do_action():

    return_code, results = lpa.do_action(provision_data)

    failed = False
    if return_code:
        failed = True
        for target, data in results.iteritems():
            task_results = data['task_results'][0]

            if not isinstance(task_results, int):
                trs = task_results
                if trs is not None:
                    trs.reverse()
                    tr = trs[0]
                    if tr.is_failed():
                        msg = tr._check_key('msg')
                        print("Target '{0}': {1} failed with"
                              " error '{2}'".format(target,
                                                    tr._task,
                                                    msg))
            else:
                if task_results:
                    return_code = task_results

    assert not failed

@with_setup(setup_lp_api)
def test_do_validation():
    return_code, results = lpa.do_validation(provision_data)

    failed = False
    if return_code:
        failed = True
        for target, data in results.iteritems():
            if not data.startswith("valid"):
                print("Validation for target '{0}': has failed with"
                      " error '{1}'".format(target, msg))

    assert not failed

@with_setup(setup_lp_api)
def test_lp_journal():

    x = lpa.lp_journal(targets=[provider])
    assert x.get(provider)


@with_setup(setup_lp_api)
def test_invoke_playbooks():

    topo = provision_data.get(provider).get('topology')
    resources = topo.get('resource_groups')

    rundb = lpa.setup_rundb()  # noqa F841
    lpa.set_evar('rundb_id', 1)

    lpa.set_evar('topo_data', topo)
    lpa.set_evar('target', provider)
    lpa.set_evar('resources', resources)
    lpa.set_evar('uhash', 'test')

    return_code, results = lpa._invoke_playbooks(resources,
                                                 action='up',
                                                 console=True)

    assert return_code == 0


def main():
    pass


if __name__ == '__main__':
    sys.exit(main())
