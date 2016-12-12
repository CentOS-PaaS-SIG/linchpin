#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Samvaran Kashyap Rallabandi -  <srallaba@redhat.com>
#
# Auth driver  for Ansible based infra provsioning tool, linch-pin
DOCUMENTATION = '''
---
version_added: "0.1"
module: auth_driver
short_description: auth_driver module in ansible
description:
  - This module allows a user to fetch credentials on request and egister it as variable in ansible.

options:
  type:
    description:
      type of credential required
    required: true

author: Samvaran Kashyap Rallabandi -
'''

import datetime
import sys
import json
import os
import shlex
import tempfile
import yaml
from ansible.module_utils.basic import *
import cloud_creds
from cloud_creds import credentials as creds

def check_file_paths(module, *args):
    for file_path in args:
        if not os.path.exists(file_path):
            module.fail_json(msg= "File not found %s not found" % (file_path))
        if not os.access(file_path, os.R_OK):
            module.fail_json(msg= "File not accesible %s not found" % (file_path))
        if os.path.isdir(file_path):
            module.fail_json(msg= "Recursive directory not supported  %s " % (file_path))

def main():
    module = AnsibleModule(
    argument_spec={
            'type':     {'required': True, 'aliases': ['auth_type']},
            'creds_store': {'required': True, 'aliases': ['credential_store']},
            'name': {'required': True, 'aliases': ['cred_name']},
            'profile': {'required': False, 'aliases': ['profile'], 'default':None},
        },
        required_one_of=[],
        supports_check_mode=True
    )
    
    ctype = module.params['type']
    cred_store_path = module.params['creds_store']
    name = module.params['name']
    profile = module.params['profile'] 
    changed = True
    output = creds.get_creds(ctype, cred_store_path, name, profile)
    if output == None:
        module.fail_json(msg="Invalid credentials path")
    module.exit_json(changed=changed, output=output)
    return output

from ansible.module_utils.basic import *
main()
