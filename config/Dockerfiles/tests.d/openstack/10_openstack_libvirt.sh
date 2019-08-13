#!/bin/bash

# Verify the openstack keypair provisioning
# distros.exclude: fedora29 fedora30 
# providers.include: openstack
# providers.exclude: none

DISTRO=${1}
PROVIDER=${2}

TARGET="os-server-new"
TEMPLATE_DATA="{\"distro\": \"linchpinlib-\"}"
TMP_FILE=$(mktemp)

function clean_up {
    set +e
    linchpin -w . -p "${PINFILE}" --template-data "${TEMPLATE_DATA}" -v destroy "${TARGET}"
}
trap clean_up EXIT SIGHUP SIGINT SIGTERM

pushd docs/source/examples/workspaces/${PROVIDER}
linchpin -w . --template-data "${TEMPLATE_DATA}" --output-pinfile "${TMP_FILE}" -v up "${TARGET}"

grep "${DISTRO}" "${TMP_FILE}"
echo "The path to linchpin libvirt key is ......."
echo $LINCHPIN_LIBVIRT_KEY

echo "current working directory is ....."
ls -l .


popd 

echo "current working directory is ....."
ls -l .

echo "compressing linchpin folder"
tar -czf linchpin.tar.gz .

echo "Install linchpin dependencies"
ssh -o StrictHostKeyChecking=no -i /workDir/workspace/ci-linchpin/linchpin/keys/linchpin_libvirt_key.pem centos@10.0.147.17 'sudo yum install libselinux-python -yq'

echo "make dir for linchpin tar files"
ssh -o StrictHostKeyChecking=no -i /workDir/workspace/ci-linchpin/linchpin/keys/linchpin_libvirt_key.pem centos@10.0.147.17 'mkdir -p /tmp/linchpin/'

echo "transfer linchpin tar files"
scp -o StrictHostKeyChecking=no -i /workDir/workspace/ci-linchpin/linchpin/keys/linchpin_libvirt_key.pem linchpin.tar.gz centos@10.0.147.17:/tmp/linchpin

echo "make dir for linchpin tar files"
ssh -o StrictHostKeyChecking=no -i /workDir/workspace/ci-linchpin/linchpin/keys/linchpin_libvirt_key.pem centos@10.0.147.17 'ls /tmp/linchpin/'

echo "extract dir"
ssh -o StrictHostKeyChecking=no -i /workDir/workspace/ci-linchpin/linchpin/keys/linchpin_libvirt_key.pem centos@10.0.147.17 'cd /tmp/linchpin/; tar -xzf linchpin.tar.gz'

echo "check the extracted files"
ssh -o StrictHostKeyChecking=no -i /workDir/workspace/ci-linchpin/linchpin/keys/linchpin_libvirt_key.pem centos@10.0.147.17 'ls /tmp/linchpin/'

echo "install PR for linchpin"
ssh -o StrictHostKeyChecking=no -i /workDir/workspace/ci-linchpin/linchpin/keys/linchpin_libvirt_key.pem centos@10.0.147.17 'sudo pip install -e /tmp/linchpin/'

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

pushd docs/source/examples/workspaces/${PROVIDER}
