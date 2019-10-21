#!/bin/bash -ex

WORKDIR=$(pwd)

pip3 install 'setuptools>=40.8.0'
pip3 install 'pyopenssl>=17.5.0'
pip3 install 'boto>=2.49.0'
pip3 install 'boto3>=1.9.96'
pip3 install 'apache-libcloud>=0.20.1'
pip3 install 'click>=7.0'
pip3 install 'yamlordereddictloader>=0.4.0'
pip3 install 'ansible>=2.7.1,<=2.9.0'
pip3 install 'six>=1.10.0'
pip3 install 'shade>=1.30.0'
pip3 install 'naked>=0.1.31'
pip3 install 'Cerberus>=1.2'
pip3 install 'tinydb>=3.12.2'
pip3 install 'requests>=2.21.0'
pip3 install 'ipaddress>=1.0.17'
pip3 install 'urllib3>=1.23,<1.25'
pip3 install 'PyYAML>=5.1'
pip3 install 'jinja2>=2.10'
pip3 install 'configparser>=3.5.0'
pip3 install 'pyasn1>=0.1.9'
pip3 install 'gitpython==2.1.11'
pip3 install 'future'

pip3 install . --ignore-installed
pip3 install .[tests]
pip3 install .[libvirt]
pip3 install .[beaker]
pip3 install .[docker]
pip3 install .[azure]
pip3 install .[openshift]

# If duffy.key is available then install duffy ansible module.
if [ -e "keys/duffy.key" ]; then
    # duffy key needs to be in home dir by default
    #cp duffy ~/duffy,key

    # Link duffy module linchpin library
    pushd ~
    linchpin_path=$(python -c 'import os, linchpin; print os.path.dirname(linchpin.__file__)')
    popd
    if [ -n "$linchpin_path" ]; then
        pushd $linchpin_path/provision/library
        ln -s $WORKDIR/duffy-ansible-module/library/duffy.py .
        popd
    fi
fi
