#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Samvaran Kashyap Rallabandi -  <srallaba@redhat.com>
#
# Ansible module to provision, deprovision openstack hot templates
import datetime
import sys
import os
import ast
from openstack import connection
from openstack import orchestration
from ansible.module_utils.basic import *


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

author: Samvaran Kashyap Rallabandi-
'''


def check_file_paths(module, *args):
    for file_path in args:
        if not os.path.exists(file_path):
            msg = "File not found %s not found" % (file_path)
            module.fail_json(msg=msg)
        if not os.access(file_path, os.R_OK):
            msg = "File not accesible %s not found" % (file_path)
            module.fail_json(msg=msg)
        if os.path.isdir(file_path):
            msg = "Recursive directory not supported  %s " % (file_path)
            module.fail_json(msg=msg)


def get_connection(auth_args):
    """ separate function for get_connection ,might change ::
        still have figureout how to access env var defaults for auth """
    con = connection.Connection(**auth_args)
    return con


def create_stack(stack_name, template, wait, parameters, auth_args):
    con = get_connection(auth_args)
    resp = con.orchestration.find_stack(stack_name)
    if not (resp is None):
        resp = resp.to_dict()
        resp['changed'] = False
        return resp
    if wait == "yes":
        output = con.orchestration.create_stack(name=stack_name,
                                                parameters=parameters,
                                                template=template)
        resp = con.orchestration.wait_for_status(output,
                                                 status='CREATE_COMPLETE',
                                                 failures=['CREATE_FAILED'])
        resp = resp.to_dict()
        resp['changed'] = True
    else:
        resp = con.orchestration.create_stack(name=stack_name,
                                              parameters=parameters,
                                              template=template)
        resp = resp.to_dict()
        resp['changed'] = True
    return resp


def delete_stack(stack_name, wait, auth_args):
    con = get_connection(auth_args)
    con.orchestration.delete_stack(stack_name)
    resp = con.orchestration.find_stack(stack_name)
    if resp is None:
        resp = {}
        resp['changed'] = True
        return resp
    else:
        resp = {}
        resp['changed'] = True
        return resp


def main():
    module = AnsibleModule(
             argument_spec=dict(
                           stack_name=dict(
                                      required=True, aliases=['name']
                           ),
                           os_username=dict(
                                       required=False, aliases=['username']
                           ),
                           os_password=dict(
                                       required=False, aliases=['password']
                           ),
                           os_tenant_name=dict(
                                          required=False,
                                          aliases=['tenantname']
                           ),
                           os_auth_url=dict(required=False, aliases=['url']),
                           template=dict(required=True),
                           state=dict(required=True),
                           wait=dict(required=False, choices=['yes', 'no']),
                           parameters=dict(required=False)
             ),
             required_one_of=[],
             supports_check_mode=True)
    stack_name = module.params['stack_name']
    state = module.params['state']
    template_path = os.path.expanduser(module.params['template'])
    check_file_paths(module, template_path)
    template = open(template_path, "r").read()
    wait = module.params['wait'] if 'wait' in module.params else "yes"
    if 'parameters' in module.params:
        parameters = ast.literal_eval(module.params['parameters'])
    else:
        parameters = None
    auth_args = {}
    if 'os_username' in module.params:
        auth_args['username'] = module.params['os_username']
    else:
        auth_args['username'] = os.environ.get('OS_USERNAME')
    if 'os_password' in module.params:
        auth_args['password'] = module.params['os_password']
    else:
        auth_args['password'] = os.environ.get('OS_PASSWORD')
    if 'os_tenant_name' in module.params:
        auth_args['project_name'] = module.params['os_tenant_name']
    else:
        auth_args['project_name'] = os.environ.get('OS_TENANT_NAME')
    if 'os_auth_url' in module.params:
        auth_args['auth_url'] = module.params['os_auth_url']
    else:
        auth_args['auth_url'] = os.environ.get('OS_AUTH_URL')
    for key in auth_args:
        if auth_args[key] is None:
            module.fail_json(msg="Auth Parameters missing")
    if state == "present":
        resp = create_stack(stack_name, template, wait, parameters, auth_args)
        resp["par"] = parameters
        module.exit_json(changed=resp['changed'], output=resp)
    elif state == "absent":
        resp = delete_stack(stack_name, wait, auth_args)
        module.exit_json(changed=resp['changed'], output=resp)

main()
