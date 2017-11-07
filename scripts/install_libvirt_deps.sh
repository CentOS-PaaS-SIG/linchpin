#!/bin/bash

dnf install libvirt-devel -yq
dnf install libguestfs-tools python-libguestfs
pip install linchpin[libvirt]


