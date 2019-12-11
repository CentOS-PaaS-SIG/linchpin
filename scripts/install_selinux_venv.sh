#!/bin/bash

DNF='dnf'
VERSION=$(python --version 2>&1 | cut -f 2 -d ' ' | sed 's/\.[0-9]*$//')
VERSION_MAJOR=$(echo ${VERSION} | awk -F '.' {'print $1'})
VERSION_MINOR=$(echo ${VERSION} | awk -F '.' {'print $2'})
grep -i fedora /etc/os-release

if [ "${?}" != 0 ]; then
    DNF='yum'
fi

VENV_LIB_PATH=lib/python${VERSION}/site-packages
LIBSELINUX_PATH=/usr/lib64/python${VERSION}/site-packages

if [ -n "${VIRTUAL_ENV}" ]; then
    if [ "${USER}" != "root" ]; then
        sudo ${DNF} install libselinux-python -yq &> /dev/null
    else
        ${DNF} install libselinux-python -yq &> /dev/null
    fi

    ln -s ${LIBSELINUX_PATH}/selinux ${VIRTUAL_ENV}/${VENV_LIB_PATH} &> /dev/null
    if [[ ${VERSION_MAJOR} -gt 2 ]]; then
      ln -s ${LIBSELINUX_PATH}/_selinux.cpython-${VERSION_MAJOR}${VERSION_MINOR}m-x86_64-linux-gnu.so ${VIRTUAL_ENV}/${VENV_LIB_PATH} &> /dev/null
    else
      ln -s ${LIBSELINUX_PATH}/_selinux.so ${VIRTUAL_ENV}/${VENV_LIB_PATH} &> /dev/null
    fi
else
    echo "A virtual environment is required"
    exit 1
fi
