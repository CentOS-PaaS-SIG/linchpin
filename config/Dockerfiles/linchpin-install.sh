#!/bin/bash -x

WORKDIR=$(pwd)

pip3 install . --ignore-installed
pip3 install .[tests]
pip3 install .[libvirt]
#pip3 install .[beaker]
#pip3 install .[docker]
pip3 install .[azure]
pip3 install .[openshift]

# If duffy.key is available then install duffy ansible module.
if [ -e "keys/duffy.key" ]; then
    # duffy key needs to be in home dir by default
    #cp duffy ~/duffy,key

    # Link duffy module linchpin library
    pushd ~
    linchpin_path=$(python3 -c 'import os, linchpin; print(os.path.dirname(linchpin.__file__))')
    popd
    if [ -n "$linchpin_path" ]; then
        pushd $linchpin_path/provision/library
        ln -s $WORKDIR/duffy-ansible-module/library/duffy.py .
        popd
    fi
fi

pushd $WORKDIR
PYTHON_VERSION=$(which python)
echo $PYTHON_VERSION
# run flake8 tests on linchpin source code
flake8 --exclude=\.eggs,tests,docs,config/Dockerfiles,duffy-ansible-module --ignore=E124,E303,W504 --max-line-length 80 .
# run unit tests
$PYTHON_VERSION ./setup.py test
popd
