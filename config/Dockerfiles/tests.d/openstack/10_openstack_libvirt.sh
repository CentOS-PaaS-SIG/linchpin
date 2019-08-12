#!/bin/bash

# check for the linchpin_libvirt_key file

echo "The path to linchpin libvirt key is ......."
echo $LINCHPIN_LIBVIRT_KEY


# installation of libvirt dependencies
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'sudo yum install libselinux-python -yq'
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'sudo yum install epel-release -yq'
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'sudo yum install python-pip -yq'

# remove if there is any existing linchpin directory
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'rm -rf /tmp/linchpin'
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'git clone https://github.com/CentOS-PaaS-SIG/linchpin /tmp/linchpin'
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'ls /tmp/linchpin'

# verify if linchpin is downloaded
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'ls /tmp/linchpin'

# update setuptools
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'sudo pip install setuptools --upgrade'
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'sudo pip uninstall linchpin'
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'sudo pip install -e file:///tmp/linchpin'
#ssh -i linchpin_libvirt.key centos@10.0.147.17 'mkdir -p /tmp/workspace; linchpin init libvirt'

