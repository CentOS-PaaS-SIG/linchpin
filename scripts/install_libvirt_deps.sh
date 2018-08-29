#!/bin/bash

if [ "${1}99" != "99" ]; then
    LP_PATH=${1}
else
    LP_PATH=${PWD}
fi

DNF='dnf'
grep -i fedora /etc/os-release

if [ "${?}" != 0 ]; then
    DNF='yum'
fi

if [ "${USER}" != "root" ]; then
    sudo ${DNF} install libvirt-devel -yq
    sudo ${DNF} install libguestfs-tools python-libguestfs -yq
else
    ${DNF} install libvirt-devel -yq
    ${DNF} install libguestfs-tools python-libguestfs -yq
fi

if [ -e "${LP_PATH}" ]; then
    pip install -e ${LP_PATH}\[libvirt\]
else
    pip install ${LP_PATH}\[libvirt\]
fi


if [ -n "${VIRTUAL_ENV}" ]; then
   ${PWD}/scripts/install_selinux_venv.sh
fi
