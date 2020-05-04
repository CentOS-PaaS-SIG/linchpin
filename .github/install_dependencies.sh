#!/usr/bin/env bash
echo "Hello this is first attempt to run bash script on github actions"
OS=$(cat /etc/*release | grep ^NAME | tr -d 'NAME="') 
ID=$(cat /etc/*release | grep ^ID | tr -d 'ID="') 
VERSION_ID=$(cat /etc/*release | grep ^VERSION_ID | tr -d 'VERSION_ID="') 

echo $OS
echo $ID
echo $VERSION_ID

if [ $VERSION_ID = "8" ]
then
    echo "This is centos8";
    export LC_ALL=C.UTF-8;
    export LANG=C.UTF-8;
    yum install -y python3 epel-release which git wget;
    yum install -y python3-pip python3-flake8 python3-devel gcc;
    yum install -y python3-pytest;
    yum install -y openssl-devel;
    yum install libvirt-devel -y;
    yum install libguestfs-tools python-libguestfs -y;
    mkdir -p /github/home/.ssh/;
elif [ $VERSION_ID = "7" ]
then
    echo "This is centos7";
    export LC_ALL="en_US";
    export LANG="en_US";
    yum install libvirt-devel -y;
    yum install -y openssl-devel;
    yum install libguestfs-tools python-libguestfs -y;
    yum install -y python3 epel-release which git wget;
    yum install -y python-pip python3-pip python3-devel gcc;
    pip install flake8;
    yum install -y pytest;
    mkdir -p /github/home/.ssh/;
else
    echo "This is fedora";
    export LC_ALL=C.UTF-8;
    export LANG=C.UTF-8;
    yum install libvirt-devel -y;
    yum install -y openssl-devel;
    yum install libguestfs-tools python-libguestfs -y;
    dnf install -y --nogpgcheck python3 git python3-pip python3-flake8 python3-devel gcc which wget;
    dnf install -y --nogpgcheck python3-pytest;
    mkdir -p /github/home/.ssh/;

fi

