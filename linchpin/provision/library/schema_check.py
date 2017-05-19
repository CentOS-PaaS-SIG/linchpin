#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Samvaran Kashyap Rallabandi -  <srallaba@redhat.com>
#
# Topology validator for Ansible based infra provsioning tool linch-pin

from ansible.module_utils.basic import *
import datetime
import sys
import json
import os
import shlex
import tempfile
import yaml
import jsonschema
from jsonschema import validate

DOCUMENTATION = '''
---
version_added: "0.1"
module: topo_check
short_description: Topology validator module in ansible
description:
  - This module allows a user to validate the yaml/json
    provisioning topologies against json schema.

options:
  data_file:
    description:
      path to topology file can be in json/yaml format
    required: true
  data_format:
    description:
      format of the topology file
    default: yaml
  schema_file:
    description:
      Schema to be validated against
    required: true

author: Samvaran Kashyap Rallabandi -
'''


class JSONSchema:
    def __init__(self, data_file_path, schema_file_path):
        self.data_file = data_file_path
        self.schema_file = schema_file_path

    def validate(self):
        data = self.get_data(self.data_file)
        schema = open(self.schema_file).read()

        try:
            result = jsonschema.validate(json.loads(data), json.loads(schema))
            return (True, json.loads(data))
        except jsonschema.ValidationError as e:
            return (False, "ValidationError: {0}".format(e.message))
        except jsonschema.SchemaError as e:
            return (False, "SchemaError: {0}".format(e))
        except Exception as e:
            return (False, "Unknown Error: {0}".format(e))

    def get_data(self, file_path):
        ext = file_path.split(".")[-1]
        if (ext == "yml" or ext == "yaml"):
            fd = open(file_path)
            return json.dumps(yaml.safe_load(fd))
        if (ext == "json"):
            return open(self.topo_file).read()
        else:
            return {"error": "Invalid File Format"}


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


def validate_grp_names(data):
    res_grps = data['resource_groups']
    if 'resource_group_vars' in data.keys():
        res_grp_vars = data['resource_group_vars']
    else:
        res_grp_vars = []
    res_grp_names = [x['resource_group_name'] for x in res_grps]
    if len(res_grp_vars) > 0:
        res_grp_vars = [x['resource_group_name'] for x in res_grp_vars]
    dup_grp_names = set(res_grp_names)
    dup_grp_vars = set(res_grp_vars)
    if len(dup_grp_vars) != len(res_grp_vars) or \
       len(dup_grp_names) != len(res_grp_names):
        msg = "error: duplicate names found in resource_group_name \
               attributes please check the results for duplicate names"
        return {"msg": msg, "result": str(dup_grp_names)+str(dup_grp_vars)}
    else:
        return True


def validate_values(module, data_file_path):
    data = open(data_file_path).read()
    data = yaml.safe_load(data)
    status = validate_grp_names(data)
    if not status:
        module.fail_json(msg="%s" % (json.dumps(status)))
    else:
        return status


def main():
    module = AnsibleModule(
    argument_spec={
            'data': {'required': True, 'aliases': ['topology']},
            'schema': {'required': True},
            'data_format': {'required': False,'choices':['json','yaml','yml']},
        },
        required_one_of=[],
        supports_check_mode=True
        )
    data_file_path = os.path.expanduser(module.params['data'])
    schema_file_path = os.path.expanduser(module.params['schema'])
    check_file_paths(module, data_file_path, schema_file_path)
    validate_values(module, data_file_path)
    schema_obj = JSONSchema(data_file_path, schema_file_path)

    status, out = schema_obj.validate()

#    module.fail_json(msg=out)

    if status:
        changed = True
        module.exit_json(isvalid=changed, out=out)
    else:
        resp = {"path": data_file_path,
                "schema": schema_file_path,
                "output": out}

        module.fail_json(msg=resp)

main()
