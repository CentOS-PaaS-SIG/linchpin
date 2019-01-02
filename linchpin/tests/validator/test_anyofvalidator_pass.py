import os
import sys
import json
import yaml

from nose.tools import assert_true
from nose.tools import with_setup

from linchpin import LinchpinAPI
from linchpin.utils.dataparser import DataParser
from linchpin.context import LinchpinContext
from linchpin.rundb import RunDB

from linchpin.validator import AnyofValidator

from linchpin.tests.mockdata.contextdata import ContextData


def setup_validator():

    """
    Perform setup of AnyofValidator, definitions, field, and value
    """

    global validator
    global topo

    lpc = LinchpinContext()
    lpc.load_config()
    lpc.load_global_evars()
    lpa = LinchpinAPI(lpc)

    schema_file = 'schema.json'
    base_path = '{0}'.format(os.path.dirname(os.path.realpath(__file__)))\
        .rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))
    sp = '{0}/{1}/{2}'.format(lib_path, 'mockdata/general', schema_file)
    schema = json.load(open(sp))

    validator = AnyofValidator(schema)

    topo_name = 'libvirt-new.yml'
    topo_file = '{0}/{1}/{2}'.format(lib_path, 'mockdata/libvirt', topo_name)
    topo = yaml.load(open(topo_file))



@with_setup(setup_validator)
def test_validate_anyof():
    document = { 'res_defs': topo['resource_groups'][0]['resource_definitions']}
    success = validator.validate(document)
    assert_true(success)


def main():
    pass


if __name__ == '__main__':
    sys.exit(main())
