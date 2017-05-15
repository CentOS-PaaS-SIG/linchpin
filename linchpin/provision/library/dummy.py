#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Clint Savage- @herlo <herlo@redhat.com>
#
# Provision a dummy server. Useful for testing the linchpin api provisioner
# without using actual resources.
#

#---- Documentation Start ----------------------------------------------------#
DOCUMENTATION = '''
---
version_added: "0.1"
module: dummy
short_description: Dummy instance managemer
description:
  - This module allows a user to manage any number of dummy systems.
options:
  name:
    description:
      Given name for task
  state:
    description:
      Allocate or Deallocate instances
    required: true

requirements: []
author: Clint Savage - @herlo
'''

EXAMPLES = '''
- name: "provision a dummy node"
  dummy:
    state: present
    name: my_dummy_node
  register: herlo-dummy-node

# teardown node named my_dummy_node
- name: "teardown dummy node"
  duffy:
    state: absent
    name: my_dummy_node

'''

#---- Logic Start ------------------------------------------------------------#
import os, re, sys, json, random, string, tempfile

from ansible.constants import mk_boolean
from ansible.module_utils.basic import *


class Dummy:

    def __init__(self):

        self.DUMMY_FILE = '{0}/dummy.hosts'.format(tempfile.gettempdir())
        pass

#    def generate_hostname(self, minlen=5, maxlen=20):
#        """
#        Generate a random hostname between minlen and maxlen, appending
#        '.example.net' (eg. oskpijsrss7.example.net)
#
#        :param minlen: minimum length of the hostname (default: 5)
#
#        :param maxlen: maximum length of the hostname (default: 20)
#        """
#
#        len = random.randint(minlen, maxlen)
#
#        host_str = ''.join(
#            random.choice(string.ascii_lowercase) for _ in range(len -1))
#
#        host_str = '{0}{1}.example.net'.format(
#                host_str, random.choice(string.digits))
#
#        return host_str


    def allocate(self, name, count=1):
        """
        Create some dummy host as if these systems existed.
        Write the host out to the dummy.hosts temporary file to avoid
        duplication.
        """

        changed = False

        hosts = []

        for i in range(count):
            host = '{0}-{1}.example.net'.format(name, i)
            with open(self.DUMMY_FILE, 'a+') as f:
                if not any('{0}\n'.format(host) in line for line in f):
                    f.write('{0}\n'.format(host))
                    changed = True
            hosts.append(host)

        return (changed, hosts)


    def deallocate(self, name, count=1):
        """
        Deallocate some dummy host.
        Remove the host from the dummy.hosts temporary file.
        """

        changed = False
        out = []
        hosts_to_del = []

        if not os.path.exists(self.DUMMY_FILE):
            return changed

        with open(self.DUMMY_FILE, 'r+') as f:
            lines = f.readlines()

            hostre = '^{0}-\d.example.net'.format(name)
            for line in lines:
                if re.search(hostre, line):
                    hosts_to_del.append(line)
                    changed = True

        num2del =  len(lines)-count
        out = hosts_to_del[0:num2del]

        with open(self.DUMMY_FILE, 'w') as f:
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
            json_output['dummy_file'] = self.DUMMY_FILE

            return json_output

        elif state == 'absent':

            status = self.deallocate(name, count)
            json_output['changed'] = status
            json_output['dummy_file'] = self.DUMMY_FILE


        return json_output

def main():

    module = AnsibleModule(
        argument_spec=dict(
            name = dict(type='str'),
            count = dict(default=1, type='int'),
            state = dict(choices=['present', 'absent']),
        ),
    )

    try:
        d = Dummy()
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


#---- Import Ansible Utilities (Ansible Framework) ---------------------------#
main()
