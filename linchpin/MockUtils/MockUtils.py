from __future__ import absolute_import
from __future__ import print_function
from six.moves import range


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
