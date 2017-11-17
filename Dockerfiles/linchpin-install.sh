#!/bin/bash -x

pushd /workdir
pip install .
pip install .[tests]
pip install .[libvirt]
popd

# If duffy.key is available then install duffy ansible module.
if [ -e "/workdir/Dockerfiles/duffy.key" ]; then
    # duffy key needs to be in home dir by default
    cp /workdir/Dockerfiles/duffy.key ~

    # Link duffy module linchpin library
    linchpin_path=$(python -c 'import os, linchpin; print os.path.dirname(linchpin.__file__)')
    if [ -n "$linchpin_path" ]; then
        pushd $linchpin_path/provision/library
        ln -s /workdir/Dockerfiles/duffy-ansible-module/library/duffy.py .
        popd
    fi
fi
