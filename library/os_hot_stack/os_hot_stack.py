#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Samvaran Kashyap Rallabandi -  <srallaba@redhat.com>
#
# Ansible module to provision, deprovision openstack hot templates
DOCUMENTATION = '''
---
version_added: "0.1"
module: os_hot_stack
short_description: ansible openstack module to provision hot templates
description:
  - This module allows a user to provision hot templates.

options:
  stack_name:
    description:
     name of the stack to be created
    required: true
  template:
    description:
      path to topology file can be in json/yaml format
    required: true
  parameters:
    description:
      parameters passed to the hot template
  state:
    description:
      state of the hot stack
  wait:
    description:
      wait for the template provision to happen 

author: Samvaran Kashyap Rallabandi -  
'''
import datetime
import sys
import os
import json
from openstack import connection
from openstack import orchestration
from ansible.module_utils.basic import *


def check_file_paths(module, *args):
    for file_path in args:
        if not os.path.exists(file_path):
            module.fail_json(msg= "File not found %s not found" % (file_path))
        if not os.access(file_path, os.R_OK):
            module.fail_json(msg= "File not accesible %s not found" % (file_path))
        if os.path.isdir(file_path):
            module.fail_json(msg= "Recursive directory not supported  %s " % (file_path))

def get_connection(auth_args):
    """ seperate function for get_connection , might change still have figure out env var defaults for auth """
    con = connection.Connection(**auth_args)
    return con

def create_stack(stack_name, template, wait, parameters,auth_args):
    """support for parameters is not tested yet"""
    con = get_connection(auth_args)
    resp = con.orchestration.find_stack(stack_name)
    if not resp == None:
        resp = resp.to_dict()
        resp['changed'] = False
        return resp
    if wait == "yes":
        output = con.orchestration.create_stack(name=stack_name, parameters={}, template=template)
        resp = con.orchestration.wait_for_status(output, status='CREATE_COMPLETE', failures=['CREATE_FAILED'])
        resp = resp.to_dict()
        resp['changed']=True
    else:
        resp = con.orchestration.create_stack(name=stack_name, parameters={}, template=template)
        resp = resp.to_dict()
        resp['changed']=True
    return resp

def delete_stack(stack_name, wait, auth_args):
    con = get_connection(auth_args)
    con.orchestration.delete_stack(stack_name)
    resp = con.orchestration.find_stack(stack_name)
    if resp == None:
        resp = {}
        resp['changed'] = True
        return resp
    else:
        resp = {}
        resp['changed'] = True
        return resp

def main():
    module = AnsibleModule(
    argument_spec={
            'stack_name':     {'required': True, 'aliases': ['name']},
            'os_username':     {'required': False, 'aliases': ['name']},
            'os_password':     {'required': False, 'aliases': ['name']},
            'os_tenant_name':     {'required': False, 'aliases': ['name']},
            'os_auth_url':     {'required': False, 'aliases': ['name']},
            'template':     {'required': True},
            'state':     {'required': True, 'choices':['present','absent']},
            'wait':     {'required': False, 'choices':['yes','no']},
            'parameters':     {'required': False},
        },
        required_one_of=[],
        supports_check_mode=True
    )
    stack_name = module.params['stack_name']
    state = module.params['state']
    template_path = os.path.expanduser(module.params['template'])
    check_file_paths(module, template_path)
    template = open(template_path,"r").read()
    wait = module.params['wait'] if 'wait' in module.params else "yes"
    parameters = module.params['parameters'] if 'parameters' in module.params else None
    auth_args = {}
    auth_args['username'] = module.params['os_username'] if 'os_username' in module.params else os.environ.get('OS_USERNAME')
    auth_args['password'] = module.params['os_password'] if 'os_password' in module.params else os.environ.get('OS_PASSWORD')
    auth_args['project_name'] = module.params['os_tenant_name'] if 'os_tenant_name' in module.params else os.environ.get('OS_TENANT_NAME')
    auth_args['auth_url'] = module.params['os_auth_url'] if 'os_auth_url' in module.params else os.environ.get('OS_AUTH_URL')
    for key in auth_args:
        if auth_args[key] == None:
            module.fail_json(msg= "Auth Parameters missing")
    if state == "present":
        resp = create_stack(stack_name, template, wait, parameters, auth_args)
        module.exit_json(changed=resp['changed'], output=resp)
    elif state == "absent":
        resp = delete_stack(stack_name, wait, auth_args)
        module.exit_json(changed=resp['changed'], output=resp)

from ansible.module_utils.basic import *
main()
