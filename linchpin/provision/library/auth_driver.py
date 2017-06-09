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
  name:
    description:
      name of the credential file to be used 
    required: true
  cred_type:
    description:
      credential type , type of credential to be used.
      eg: aws, gcloud , openstack , etc.,
    required: false
  cred_path:
    description:
      credentials path where the credentials are to be stored
    required: false
  driver:
    description:
      defaults to file type. 
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
import glob

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser as ConfigParser


class ConfigDict(ConfigParser.ConfigParser):

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


def parse_file(filename):
    cred_str = open(filename, "r").read()
    try:
        out = json.loads(cred_str)
    except Exception as e:
        try:
            out = yaml.load(cred_str)
        except Exception as e:
            try:
                config = ConfigDict()
                f = open(filename)
                config.readfp(f)
                out = config.as_dict()
                f.close()
            except Exception as e:
                module.fail_json(msg= "Error  {0} ".format(str(e)))
    return out


def get_cred(fname, creds_path):

    paths = creds_path.split(os.path.pathsep)
    files = []
    for path in paths:
        path = os.path.realpath(os.path.expanduser(path))
        for filename in os.listdir(path):
            if fname == filename:
                full_file_path = '{0}/{1}'.format(path, filename)
                out = parse_file(full_file_path)
                return out, path

    module.fail_json(msg= "Error: Credential not found")


def main():

    global module
    module = AnsibleModule(
    argument_spec={
            'filename': {'required': True, 'aliases': ['name']},
            'cred_type': {'required': False, 'aliases': ['credential_type']},
            'cred_path': {'required': True, 'aliases': ['credential_store']},
            'driver': {'required': True, 'aliases': ['driver_type']},
        },
        required_one_of=[],
        supports_check_mode=True
    )
    filename = module.params["filename"]
    cred_type = module.params["cred_type"]
    cred_path = module.params["cred_path"]
    driver_type = module.params["driver"]
    output, path = get_cred(filename, cred_path)
    changed = True
    module.exit_json(changed=changed, output=output, params=module.params, path=path)

main()
