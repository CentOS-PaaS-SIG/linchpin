#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import os

from ansible.module_utils.basic import AnsibleModule

from bkr.common.hub import HubProxy
from bkr.common.pyconfig import PyConfigParser


BEAKER_CONF = os.environ.get('BEAKER_CONF', '/etc/beaker/client.conf')


class BeakerDistro(object):
    def __init__(self, logger=None):
        self.conf = PyConfigParser()
        default_config = os.path.expanduser(BEAKER_CONF)
        self.conf.load_from_file(default_config)
        self.hub = HubProxy(logger=logger, conf=self.conf)

    def search(self, params):
        return self.hub.distros.filter(params)


def main():

    argument_spec = dict(
        name=dict(type='str', required=False),
        arch=dict(type='str', required=False),
        family=dict(type='str', required=False),
        tags=dict(type='list', required=False),
        limit=dict(type='int', required=False, default=1),
    )
    mod = AnsibleModule(argument_spec)
    beaker = BeakerDistro()
    try:
        results = beaker.search(mod.params)
        mod.exit_json(hosts=results, changed=True)
    except Exception as ex:
        mod.fail_json(msg=str(ex), changed=True)


# import module snippets
main()
