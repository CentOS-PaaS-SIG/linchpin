#!/usr/bin/env python

import os
from ansible.module_utils.basic import *

def main():
    module = AnsibleModule(
        argument_spec={
            'jenkins_home': { 'required': True }
        }
    )
    jenkins_cfg = os.path.join(module.params['jenkins_home'], 'config.xml')
    # There can be no security if there is no config.xml
    if not os.path.exists(jenkins_cfg):
        module.exit_json(changed=False, ansible_facts={'jenkins_security_enabled': False})
    # If there is a file, then query it
    with open(jenkins_cfg, 'r') as cfg:
        for line in cfg.readlines():
            # This text in a file means that security is not configured
            if "AuthorizationStrategy$Unsecured" in line:
                module.exit_json(changed=False, ansible_facts={'jenkins_security_enabled': False})
    # Default assumption is that we do want security
    module.exit_json(changed=False, ansible_facts={'jenkins_security_enabled': True})

main()
