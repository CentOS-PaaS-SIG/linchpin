#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: samvarankashyap- @samvarankashyap <skr@redhat.com>
#
# Provision a nummy server. Useful for testing the linchpin api provisioner
# without using actual resources. This is a clone of @herlo 's dummy provider
# in linchpin

import os
import re
import tempfile

from ansible.module_utils.basic import AnsibleModule

# ---- Documentation Start ----------------#
DOCUMENTATION = '''
---
version_added: "0.1"
module: nummy
short_description: Dummy clone instance managemer
description:
  - This module allows a user to manage any number of nummy systems.
options:
  name:
    description:
      Given name for task
  state:
    description:
      Allocate or Deallocate instances
    required: true

requirements: []
author: samvaran kashyap @samvarankashyap
'''

EXAMPLES = '''
- name: "provision a nummy node"
  nummy:
    state: present
    name: my_nummy_node
  register: nummy-node

# teardown node named my_nummy_node
- name: "teardown nummy node"
  duffy:
    state: absent
    name: my_nummy_node

'''

# ---- Logic Start ----------------------#


class Nummy:

    def __init__(self):

        self.NUMMY_FILE = '{0}/nummy.hosts'.format(tempfile.gettempdir())


    def allocate(self, name, count=1):
        """
        Create some nummy host as if these systems existed.
        Write the host out to the nummy.hosts temporary file to avoid
        duplication.
        """

        changed = False

        hosts = []

        for i in range(count):
            host = '{0}-{1}.example.net'.format(name, i)
            with open(self.NUMMY_FILE, 'a+') as f:
                if not any('{0}\n'.format(host) in line for line in f):
                    f.write('{0}\n'.format(host))
                    changed = True
            hosts.append(host)

        return (changed, hosts)


    def deallocate(self, name, count=1):
        """
        Deallocate some nummy host.
        Remove the host from the nummy.hosts temporary file.
        """

        changed = False
        out = []
        hosts_to_del = []

        if not os.path.exists(self.NUMMY_FILE):
            return changed

        with open(self.NUMMY_FILE, 'r+') as f:
            lines = f.readlines()

            hostre = r'^{0}-\d.example.net'.format(name)
            for line in lines:
                if re.search(hostre, line):
                    hosts_to_del.append(line)
                    changed = True

        num2del = len(lines) - count
        out = hosts_to_del[0:num2del]

        with open(self.NUMMY_FILE, 'w') as f:
            f.writelines(out)

        return changed


    def execute(self, module):

        json_output = {}
        name = module.params['name']
        state = module.params['state']
        count = module.params['count']

        # allocate some systems if state is 'present' :)
        if state == 'present':

            changed, hosts = self.allocate(name, count)
            json_output['changed'] = changed
            json_output['hosts'] = hosts
            json_output['nummy_file'] = self.NUMMY_FILE

            return json_output

        elif state == 'absent':

            status = self.deallocate(name, count)
            json_output['changed'] = status
            json_output['nummy_file'] = self.NUMMY_FILE


        return json_output


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str'),
            count=dict(default=1, type='int'),
            state=dict(choices=['present', 'absent']),
        ),
    )

    try:
        d = Nummy()
        execute_output = d.execute(module)

        json_output = {}
        host = execute_output.get('host')
        changed = execute_output.get('changed')
        if host or changed is not None:
            json_output['changed'] = True
            json_output.update(execute_output)
        else:
            json_output['changed'] = False

        module.exit_json(**json_output)
    except Exception as e:
        module.fail_json(msg=str(e))


# ---- Import Ansible Utilities (Ansible Framework) -------------------#
main()
