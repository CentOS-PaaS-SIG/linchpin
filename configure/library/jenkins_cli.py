#!/bin/bash

from shlex import split
from subprocess import Popen, PIPE
from ansible.module_utils.basic import *

def main():
    module = AnsibleModule(
        argument_spec={
            'command': {'required': True},
            'arguments': {'default': ''},
            'working_dir': {'default': '~/'},
            'use_ssl': {'type': 'bool', 'default': True},
            'validate_certs': {'type': 'bool', 'default': True},
            'server': {'default': 'localhost'},
            'server_path': {'default': '/'}
        }
    )
    jar = os.path.join(os.path.expanduser(module.params['working_dir']), 'jenkins-cli.jar')
    # Check JAR exists before proceeding
    if not os.path.exists(jar):
        module.fail_json(msg='jenkins-cli.jar not found in specified working_dir: {0}'.format(module.params['working_dir']))
    # Construct arguments
    arguments = ['java', '-jar', jar]
    # Constrcut server URL to hit
    if module.params['use_ssl']:
        protocol = 'https'
    else:
        protocol = 'http'
    server = '{0}://{1}{2}'.format(protocol, module.params['server'], module.params['server_path'])
    arguments.extend(['-s', server])
    # validate SSL certificates, if necessary
    if not module.params['validate_certs']:
        arguments.append('-noCertificateCheck')
    # add user arguments
    arguments.append(module.params['command'])
    arguments.extend(split(module.params['arguments']))
    # Execute command
    command = Popen(arguments, stdout=PIPE, stderr=PIPE)
    out, err = command.communicate()
    if command.returncode != 0:
        module.fail_json(msg='Command failed. Return code was {0}'.format(command.returncode), returncode=command.returncode, stdout=out, stderr=err)
    else:
        module.exit_json(changed=True, stdout=out, stderr=err)

    
main()
