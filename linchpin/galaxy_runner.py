from __future__ import absolute_import

import subprocess


def install(package):
    cmd = "ansible-galaxy install {0}".format(package)
    retcode = subprocess.call(cmd,
                              shell=True)

    return retcode == 0


def get_role_paths():
    """
    Returns a list of all the roles paths which Ansible-galaxy uses when
    searching for roles

    In the future, we should read the ansible.cfg and combine it with
    linchpin.conf, since this data is set in ansible.cfg.
    """
    """
    [WARNING]: - the configured path /usr/share/ansible/roles does not exist.

    [WARNING]: - the configured path /etc/ansible/roles does not exist.
    """
    paths = []

    cmd = "ansible-galaxy list"
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc.wait()

    for line in proc.stdout:
        if line.startswith(b'#'):
            path = line[2:].strip()
            paths.append(path.decode('utf-8'))

    paths.extend(["/usr/share/ansible/roles",
                  "/etc/ansible/roles"])
    return paths
