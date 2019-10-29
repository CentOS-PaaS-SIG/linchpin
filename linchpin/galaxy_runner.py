from __future__ import absolute_import

import subprocess

import ansible.constants as ansible_constants


def install(package):
    cmd = "ansible-galaxy install {0}".format(package)
    retcode = subprocess.call(cmd,
                              shell=True)

    return retcode == 0


def get_role_paths():
    """
    Returns a list of all the roles paths which Ansible-galaxy uses when
    searching for roles

    This is wrapped in a function so that the logic can be expanded/modified in
    the future if need be
    """
    return ansible_constants.DEFAULT_ROLES_PATH
