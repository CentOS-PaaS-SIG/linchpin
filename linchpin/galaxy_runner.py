from __future__ import absolute_import

import subprocess


def galaxy_runner(package):
    cmd = "ansible-galaxy install {0}".format(package)
    retcode = subprocess.call(cmd,
                              shell=True)

    return retcode == 0
