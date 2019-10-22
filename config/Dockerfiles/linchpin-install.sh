#!/bin/bash -ex

WORKDIR=$(pwd)

# test virtual environment installation
#python3 -m venv ./testenv;

#source ./testenv/bin/activate;
pip3 install .;
pip3 install .[tests];
#pip3 install .[libvirt];
#pip3 install .[beaker];
pip3 install .[docker];
pip3 install .[azure];
pip3 install .[openshift];

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
