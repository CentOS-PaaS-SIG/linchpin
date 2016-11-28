#!/usr/bin/env python
#
# Author: Greg Hellings - <ghelling@redhat.com> or <greg.hellings@gmail.com>
#
# Module to configure users in Jenkins authorized to use CLI
DOCUMENTATION = '''
---
version_added: "2.1"
module: jenkins_cli_user
short_description: configure Jenkins CLI users with pub key
description:
  - This module configures admin users in Jenkins to utilize the specified
    SSH pubkey. Requires that role-based authentication be enabled and that
    a user be configured as an admin

options:
  jenkins_home:
    description:
     The root directory for the Jenkins install
    required: true
  key_file:
    description:
      Path to the SSH keyfile to be listed as authorized
    required: true
  state:
    description:
      Currently limited to "present" - will create the user
    required: false

author: Gregory Hellings
'''

import xml.etree.ElementTree as ET
import os
import sys
from ansible.module_utils.basic import *

def main():
    module = AnsibleModule(
        argument_spec={
            'jenkins_home': { 'required': True },
            'key_file': { 'required': True },
            'state': { 'choices': ['present'], 'default': 'present' }
        },
        supports_check_mode=False
    )
    jenkins_config = os.path.join(module.params['jenkins_home'], "config.xml")
    user_config_path = os.path.join(module.params['jenkins_home'], "users" )
    tree = ET.parse(jenkins_config)
    root = tree.getroot()
    roles = root.getiterator("role")
    changed = False
    if roles:
        for role in roles:
            name = role.attrib.get("name")
            if name == "admin":
                pub_key = os.popen("cat {0}".format(module.params['key_file'])).read()
                for sid in role.getiterator("sid"):
                    user_cfg_file = os.path.join(user_config_path, sid.text, "config.xml")
                    usertree = ET.parse(user_cfg_file)
                    userroot = usertree.getroot()
                    keyroot = userroot.find("properties")
                    keys = keyroot.getiterator("authorizedKeys")
                    if keys:
                        for key in keys:
                            if pub_key not in str(key.text):
                                changed = True
                                if key.text is None:
                                    key.text = pub_key
                                else:
                                    key.text = str(key.text) + pub_key
                    else:
                        changed = True
                        prop = userroot.find("properties")
                        ssh_auth = ET.SubElement(prop,
                                                 "org.jenkinsci.main.modules"
                                                 ".cli.auth.ssh."
                                                 "UserPropertyImpl")
                        auth_key = ET.SubElement(ssh_auth, "authorizedKeys")
                        auth_key.text = pub_key
        if changed:
            usertree.write(user_cfg_file, encoding="UTF-8")
        module.exit_json(changed=changed)
    else:
        module.fail_json(msg="Roles not found - have you configured an admin using "
                " the Role-based Authorization Strategy?")

from ansible.module_utils.basic import *
main()
