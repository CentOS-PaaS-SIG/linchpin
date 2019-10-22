from __future__ import absolute_import
from __future__ import print_function
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
from linchpin.linchpin_rundb import RunDB

from linchpin.tests.mockdata.contextdata import ContextData
import six

import json
import linchpin
from linchpin.api import Pinfile
from linchpin.api import Workspace


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


def setup_api():
    """
    performs initialization required for linchpin api
    """

    global wksp
    global pfile
    base_path = '{0}'.format(os.path.dirname(os.path.realpath(__file__)))\
        .rstrip('/')
    wksp = Workspace(path=base_path+"/mockdata/api_workspace")
    pinfile = open(base_path+"/mockdata/api_workspace/PinFile","r").read()
    pinfile = json.loads(pinfile)
    pfile = Pinfile(pinfile=pinfile)



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
        for target, data in six.iteritems(results):
            task_results = data['task_results'][0]

            if not isinstance(task_results, int):
                trs = task_results
                if trs is not None:
                    trs.reverse()
                    tr = trs[0]
                    if tr.is_failed():
                        msg = tr._check_key('msg')
                        print(("Target '{0}': {1} failed with"
                              " error '{2}'".format(target,
                                                    tr._task,
                                                    msg)))
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
        for target, data in six.iteritems(results):
            if not data.startswith("valid"):
                print(("Validation for target '{0}': has failed with"
                      " error '{1}'".format(target, msg)))

    assert not failed

@with_setup(setup_lp_api)
def test_lp_journal():

    x = lpa.lp_journal(targets=[provider])
    assert x.get(provider)

"""
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
    lpa.set_evar('use_uhash', True)

    return_code, results = lpa._invoke_playbooks(resources,
                                                 action='up',
                                                 console=True)

    assert return_code == 0

"""

"""

class Workspace:

    def set_workspace(self, path):

        self.workspace_path = path
        self.context.set_cfg('lp', 'workspace', self.workspace_path )
        self.context.set_evar('workspace', self.workspace_path)
        return self.workspace_path

    def set_evar(self, key, value):

        self.context.set_evar(key, value)
        return key,value

    def set_credentials_path(self, creds_path):
        if os.path.isdir(creds_path):
            return self.context.set_evar("default_credentials_path",
                                         creds_path)
        raise LinchpinError("Incorrect file path, path should be a directory")

    def set_vault_encryption(self, vault_enc):
        if isinstance(vault_enc, bool):
            return self.context.set_evar("vault_password",vault_pass)
        raise LinchpinError("Incorrect datatype please use boolean")

    def set_no_hooks(self, flag):
        if isinstance(flag, bool):
            return self.ctx.set_cfg("hookflags", "no_hooks", flag)
        raise LinchpinError("Incorrect datatype please use boolean")

    def set_ignore_failed_hooks(self, flag):
        if isinstance(flag, bool):
            return self.ctx.set_cfg("hookflags", "ignore_failed_hooks", flag)
        raise LinchpinError("Incorrect datatype please use boolean")

    def set_vault_pass(self, vault_pass):
        return self.context.set_evar("vault_password",vault_pass)

"""
@with_setup(setup_api)
def test_api_workspace():
    assert_equal(isinstance(wksp, Workspace), True)

@with_setup(setup_api)
def test_api_pinfile():
    assert_equal(isinstance(pfile, Pinfile), True)

@with_setup(setup_api)
def test_api_wksp_load_data():
    pindict = wksp.load_data(wksp.find_pinfile())
    expected = json.loads(open(wksp.find_pinfile(), "r").read())
    assert_equal(expected, pindict)

@with_setup(setup_api)
def test_api_wksp_validate():
    out = wksp.validate()
    expected = (0, {'dummy-test': {'layout': 'valid', 'topology': 'valid'}})
    assert_equal(expected, out)
    pass

@with_setup(setup_api)
def test_api_wksp_find_pinfile():
    assert_equal(os.path.isfile(wksp.find_pinfile()), True)
    pass

@with_setup(setup_api)
def test_api_wksp_set_workspace():
    out = wksp.set_workspace("/tmp/")
    assert_equal( out, "/tmp/")

@with_setup(setup_api)
def test_api_wksp_set_evar():
    wksp.set_evar("test", "var")
    assert_equal(wksp.get_evar("test"), "var")

@with_setup(setup_api)
def test_api_wksp_set_credentials_path():
    wksp.set_credentials_path("/tmp/")
    assert_equal(wksp.get_credentials_path(), "/tmp/")

@with_setup(setup_api)
def test_api_wksp_set_vault_encryption():
    wksp.set_vault_encryption(True)
    assert_equal(wksp.get_vault_encryption(), True)

@with_setup(setup_api)
def test_api_wksp_set_flag_no_hooks():
    wksp.set_flag_no_hooks(True)
    assert_equal(wksp.get_flag_no_hooks(), True)

@with_setup(setup_api)
def test_api_wksp_set_flag_ignore_failed_hooks():
    wksp.set_flag_ignore_failed_hooks(True)
    assert_equal(wksp.get_flag_ignore_failed_hooks(), True)

@with_setup(setup_api)
def test_api_wksp_set_vault_pass():
    wksp.set_vault_pass("hello")
    assert_equal(wksp.get_vault_pass(), "hello")

@with_setup(setup_api)
def test_api_wksp_get_inventory():
    wksp.up()
    inven = wksp.get_inventory()
    assert_equal.__self__.maxDiff = None
    expected = {u'dummy-test': '{"test": {"hosts": ["web-0"]}, "all": {"hosts": ["web-0", "web-1", "web-2", "test"], "vars": {"ansible_user": "root"}}, "example": {"hosts": ["web-1", "web-2", "test"]}, "_meta": {"hostvars": {"test": "test", "web-0": "web-0", "web-1": "web-1", "web-2": "web-2"}}}'}
    expected = json.loads(expected['dummy-test']).get("all").get("hosts")
    inven = json.loads(inven['dummy-test']).get("all").get("hosts")
    assert_equal(inven, expected)

@with_setup(setup_api)
def test_api_pinfile_get_inventory():
    pfile.up()
    inven = pfile.get_inventory()
    assert_equal.__self__.maxDiff = None
    expected = {u'dummy-test': '{"test": {"hosts": ["web-0"]}, "all": {"hosts": ["web-0", "web-1", "web-2", "test"], "vars": {"ansible_user": "root"}}, "example": {"hosts": ["web-1", "web-2", "test"]}, "_meta": {"hostvars": {"test": "test", "web-0": "web-0", "web-1": "web-1", "web-2": "web-2"}}}'}
    expected = json.loads(expected['dummy-test']).get("all").get("hosts")
    inven = json.loads(inven['dummy-test']).get("all").get("hosts")
    assert_equal(inven, expected)

@with_setup(setup_api)
def test_api_pinfile_validate():
    out = pfile.validate()
    expected = (0, {'dummy-test': {'layout': 'valid', 'topology': 'valid'}})
    assert_equal(expected, out)

@with_setup(setup_api)
def test_api_wksp_up():
    out = wksp.up()
    assert_equal(len(out), 2)

@with_setup(setup_api)
def test_api_wksp_destroy():
    out = wksp.destroy()
    assert_equal(len(out), 2)

@with_setup(setup_api)
def test_api_pinfile_up():
    out = pfile.up()
    assert_equal(len(out), 2)
    pass

@with_setup(setup_api)
def test_api_pinfile_destroy():
    out = pfile.destroy()
    assert_equal(len(out), 2)
    pass

def main():
    pass


if __name__ == '__main__':
    sys.exit(main())
