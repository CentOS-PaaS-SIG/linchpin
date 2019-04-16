import os
import json
import yaml

from nose.tools import assert_true
from nose.tools import assert_equal
from nose.tools import with_setup

from linchpin import LinchpinAPI
from linchpin.context import LinchpinContext

from linchpin.validator import Validator


def setup_validator():

    """
    Perform setup of Validator,
    """

    global validator
    global pinfile

    lpc = LinchpinContext()
    lpc.load_config()
    lpc.load_global_evars()
    lpa = LinchpinAPI(lpc)
    validator = Validator(lpa.ctx, lpa.pb_path, lpa.pb_ext)

    schema_file = 'schema.json'
    base_path = '{0}'.format(os.path.dirname(os.path.realpath(__file__)))\
        .rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    sp = '{0}/{1}/{2}'.format(lib_path, '../provision/roles/dummy/files', schema_file)
    schema = json.load(open(sp))

    pf_name = 'PinFile-complete.yml'
    pf_file = '{0}/{1}/{2}'.format(lib_path, 'mockdata/dummy', pf_name)
    pinfile = yaml.load(open(pf_file))


def setup_old_topology():
    global old_topology

    pf_name = "PinFile-old.yml"
    base_path = '{0}'.format(os.path.dirname(os.path.realpath(__file__)))\
        .rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    pf_file = '{0}/{1}/{2}'.format(lib_path, 'mockdata/dummy', pf_name)
    old_topology = yaml.load(open(pf_file))['dummy-new']['topology']


@with_setup(setup_validator)
def test_validate():
    validator.validate(pinfile['dummy-new'])


@with_setup(setup_validator)
def test_validate_pretty():
    results = validator.validate_pretty(pinfile['dummy-new'], 'dummy-new')
    assert_true(results)


@with_setup(setup_validator)
def test_validate_topology():
    success = False
    topo_data = pinfile['dummy-new']['topology']
    try:
        resources = validator.validate_topology(topo_data)
        success = len(resources)
    except Exception:
        pass

    assert success


@with_setup(setup_validator)
def test_validate_layout():
    success = False
    layout_data = pinfile['dummy-new']['layout']

    validator.validate_layout(layout_data)


@with_setup(setup_validator)
def test_validate_resource_group():
    success = False
    res_grp = pinfile['dummy-new']['topology']['resource_groups'][0]

    # this will pass unless an exception is thrown
    validator.validate_resource_group(res_grp)


@with_setup(setup_validator)
def test_validate_cfgs():
    pass

@with_setup(setup_validator)
def test_find_playbook_path():
    pb_path = validator._find_playbook_path('dummy')

    assert os.path.exists(os.path.expanduser(pb_path))


def test_gen_error_msg():
    error = {'res_defs': [{0: [{u'name': ["field 'name' is required"]}]}]}

    error_msg = validator._gen_error_msg('', '', error)
    expected_msg = "res_defs[0][name]: field 'name' is required\n"

    assert_equal(error_msg, expected_msg)

@with_setup(setup_validator)
@with_setup(setup_old_topology)
def test_convert_topology():
    print old_topology
    validator._convert_topology(old_topology)
    assert_equal(old_topology, pinfile['dummy-new']['topology'])
