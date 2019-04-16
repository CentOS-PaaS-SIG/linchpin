#!/usr/bin/env python


def prepare_ssh_args(ssh_args, users, sshkey):
    # "{{ ssh_args }} --ssh-inject \
    # {{ item.0}}:string:'{{ pubkey_local.stdout }}'"
    for user in users:
        ssh_args += "--ssh-inject " + user + ":string:'" + sshkey + "' "
    return ssh_args


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'prepare_ssh_args': prepare_ssh_args
        }
