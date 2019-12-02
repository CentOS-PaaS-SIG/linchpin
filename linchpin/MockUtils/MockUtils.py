from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import os
import json


def get_dummy_mock_data(module_args):
    hosts = [module_args['name'] + "-" + str(x)
             for x in range(0, int(module_args['count']))]
    data = {
        "changed": True,
        "dummy_file": "/tmp/dummy.hosts",
        "failed": False,
        "hosts": hosts,
        "output_type": "mock"
    }
    return data


def get_openstack_mock_data(module_args, module_name):
    dirname, filename = os.path.split(os.path.abspath(__file__))
    data = open(dirname + "/" + module_name + ".data", "r").read()
    data = json.loads(data)
    return data
