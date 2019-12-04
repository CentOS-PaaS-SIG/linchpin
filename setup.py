#!/usr/bin/env python

from __future__ import absolute_import

import ast
import io
import os

from setuptools import setup, find_packages

with open('linchpin/version.py') as f:
    for line in f:
        if line.startswith('__version__'):
            ver = ast.parse(line).body[0].value.s
            break

dir_path = os.path.dirname(os.path.realpath(__file__))

# reading description from README.rst
with io.open(os.path.join(dir_path, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# reading requirements from requirements.txt
with io.open(os.path.join(dir_path, 'requirements.txt')) as f:
    required = f.read().splitlines()

install_required = list(required)

ignore_dir = ['.git']

azure_deps = open("requirements-azure.txt", "r").readlines()

setup(
    name='linchpin',
    version=ver,
    description='Ansible-based multi-cloud provisioner',
    long_description=long_description,
    author='samvaran kashyap rallabandi',
    author_email='linchpin@redhat.com',
    url='http://linchpin.readthedocs.io/',
    install_requires=install_required,
    entry_points='''
        [console_scripts]
        linchpin=linchpin.shell:runcli
    ''',
    tests_require=["pytest<=4.4.0", "nose", "mock", "coverage", "flake8"],
    extras_require={
        'krbV': ["python-krbV"],
        'beaker': ['beaker-client>=23.3', 'python-krbV'],
        'docs': ["docutils", "sphinx", "sphinx_rtd_theme", "sphinx-automodapi"],
        'tests': ["nose", "mock", "coverage", "flake8", "pytest<=4.4.0"],
        'libvirt': ["libvirt-python>=3.0.0", "lxml"],
        'vmware': ["PyVmomi>=6.7.1"],
        'docker': ["docker-py>=1.7.0"],
        'azure': azure_deps,
        'openshift': ['openshift>=0.8.6,<0.8.8']
    },
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    scripts=[
        'scripts/install_libvirt_deps.sh',
        'scripts/install_selinux_venv.sh'
    ]
)
