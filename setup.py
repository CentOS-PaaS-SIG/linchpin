#!/usr/bin/env python

import os
import ast
from setuptools import setup, find_packages

with open('linchpin/version.py') as f:
    for line in f:
        if line.startswith('__version__'):
            ver = ast.parse(line).body[0].value.s
            break

# reading requirements from requirements.txt
dir_path = os.path.dirname(os.path.realpath(__file__))
reqs_file = 'requirements.txt'.format(dir_path)
with open(reqs_file) as f:
    required = f.read().splitlines()

ignore_dir = ['.git']

setup(
    name='linchpin',
    version=ver,
    description='Ansible based multi cloud orchestrator',
    author='samvaran kashyap rallabandi',
    author_email='linchpin@redhat.com',
    url='http://linchpin.readthedocs.io/',
    setup_requires=required,
    install_requires=required,
    entry_points='''
        [console_scripts]
        linchpin=linchpin.shell:runcli
    ''',
    extras_require={
        'krbV': ["python-krbV"],
        'beaker': ['beaker-client>=23.3', 'python-krbV'],
        'docs': ["docutils", "sphinx", "sphinx_rtd_theme"],
        'tests': ["nose", "mock", "coverage", "flake8"],
        'libvirt': ["libvirt-python>=3.0.0", "lxml"],
    },
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': [
            'linchpin.constants',
        ],
    },
    scripts=[
        'scripts/install_libvirt_deps.sh',
        'scripts/install_selinux_venv.sh'
    ]
)
