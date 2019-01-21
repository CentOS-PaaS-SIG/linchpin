#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Samvaran Kashyap Rallabandi -  <srallaba@redhat.com>
#

import os
import yaml

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
version_added: "0.1"
module: output_parser
short_description: output_parser module in ansible
description:
  - This module allows a user to parse a yaml file
    and register it as variable in ansible.

options:
  output_file:
    description:
      path to topology output file can be in json/yaml format
    required: true

author: Samvaran Kashyap Rallabandi -
'''


def check_file_paths(module, *args):
    for file_path in args:
        if not os.path.exists(file_path):
            output = "File not found %s not found"
            module.fail_json(msg=output % (file_path))
        if not os.access(file_path, os.R_OK):
            output = "File not accesible %s not found"
            module.fail_json(msg=output % (file_path))
        if os.path.isdir(file_path):
            output = "Recursive directory not supported  %s "
            module.fail_json(msg=output % (file_path))


def main():
    module = AnsibleModule(
        argument_spec=dict(output_file=dict(required=True,
                                            aliases=[
                                                'topology_output_file',
                                                'resources_file'
                                            ])),
        required_one_of=[],
        supports_check_mode=True)

    data_file_path = os.path.expanduser(module.params['output_file'])

    check_file_paths(module, data_file_path)
    content = open(data_file_path, "r").read()
    c = yaml.load(content)
    resp = {"path": data_file_path, "content": c}
    if resp["content"] or resp["content"] == []:
        changed = True
        module.exit_json(changed=changed, output=resp)
    else:
        module.fail_json(msg=resp)


main()
