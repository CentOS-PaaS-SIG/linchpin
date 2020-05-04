#!/usr/bin/env bash
echo "Hello this is first attempt to run linchpin provisioning in github actions"


VERSION_ID=$(cat /etc/*release | grep ^VERSION_ID | tr -d 'VERSION_ID="')

echo $VERSION_ID

if [ $VERSION_ID = "7" ]
then
    echo "This is centos7";
    export LC_ALL="en_US.utf8";
    export LANG="en_US.utf8";
fi


linchpin --version;

mkdir /tmp/workspace/;
mkdir /root/.ssh/;

cd /tmp/workspace/;

echo $PWD;

locale -a;

echo $LC_ALL;
export $LANG;

echo "RUNNING LIBVIRT MOCK TESTS";

linchpin init libvirt;
cd libvirt;
wget -O linchpin.conf https://raw.githubusercontent.com/CentOS-PaaS-SIG/linchpin/develop/docs/source/examples/workspaces/linchpin-mock.conf;
linchpin -vvvv up libvirt-custom-xml;
linchpin -vvvv destroy libvirt-custom-xml;
