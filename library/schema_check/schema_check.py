#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Samvaran Kashyap Rallabandi -  <srallaba@redhat.com>
#
# Topology validator for Ansible based infra provsioning tool linch-pin
DOCUMENTATION = '''
---
version_added: "0.1"
module: topo_check
short_description: Topology validator module in ansible
description:
  - This module allows a user to validate the yaml/json provisioning topologies against json schema.

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

class JSONSchema:
    def __init__(self, data_file_path, schema_file_path):
        self.data_file = data_file_path
        self.schema_file = schema_file_path
    def validate(self):
        data = self.get_data(self.data_file)
        schema = open(self.schema_file).read()
        if type(data) is dict:
            return data
        try:
            result = jsonschema.validate(json.loads(data), json.loads(schema))
            return {"status":True, "data":json.loads(data)}
        except jsonschema.ValidationError as e:
            return {"error": e.message, "status":False}
        except jsonschema.SchemaError as e:
            return {"error": e, "status": False }
        except Exception as e:
            return {"error": e, "status": False }
            
    def get_data(self,file_path):
        if (file_path.split(".")[-1]=="yml" or "yaml"):
            fd = open(file_path)
            return json.dumps(yaml.safe_load(fd))
        if (file_path.split(".")[-1]=="json"):
            return open(self.topo_file).read()
        else:
            return {"error":"Invalid File Format"}

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
            'data':     {'required': True, 'aliases': ['topology_file']},
            'schema':     {'required': True, 'aliases': ['topology_file']},
            'data_format':     {'required': False,'choices':['json','yaml','yml']},
        },
        required_one_of=[],
        supports_check_mode=True
    )
    data_file_path = os.path.expanduser(module.params['data'])
    schema_file_path = os.path.expanduser(module.params['schema'])
    check_file_paths(module, data_file_path, schema_file_path)
    schema_obj = JSONSchema(data_file_path, schema_file_path)
    output = schema_obj.validate()
    resp = {"path": data_file_path, "content":output}
    if output["status"]:
         changed = True
         module.exit_json(isvalid=changed, output=output)
    else:
         module.fail_json(msg=resp)

from ansible.module_utils.basic import *
main()
