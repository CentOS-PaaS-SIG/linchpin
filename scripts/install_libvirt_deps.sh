#!/bin/bash

if [ $# -lt 1 ]; then
  echo "Usage $0 <lp-path>"
  echo
  echo lp-path: path to linchpin source
  exit 1
fi

LP_PATH=${1}

VENV_LIB_PATH=lib/python2.7/site-packages
LIBSELINUX_PATH=/usr/lib64/python2.7/site-packages

if [ -n "${VIRTUAL_ENV}" ]; then

    if [ "${USER}" != "root" ]; then
        sudo dnf install libvirt-devel libselinux-python -yq &> /dev/null
    else
        dnf install libvirt-devel libselinux-python -yq &> /dev/null
    fi

    ln -s ${LIBSELINUX_PATH}/selinux ${VIRTUAL_ENV}/${VENV_LIB_PATH} &> /dev/null
    ln -s ${LIBSELINUX_PATH}/_selinux.so ${VIRTUAL_ENV}/${VENV_LIB_PATH} &> /dev/null

    pip install ${LP_PATH}\[libvirt\]


else

    echo "A virtual environment is recommended"
    exit 1

fi
