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
mkdir -p /github/home/.azure/
echo "{}" > /github/home/.azure/azureProfile.json
cd /tmp/workspace/;

echo $PWD;

locale -a;

echo $LC_ALL;
export $LANG;
echo "RUNNING Azure MOCK TESTS";
linchpin init azure;
cd azure;
linchpin -vvvv up;
if [ $? -ne 0 ]
then
    echo "Azure tests failed on linchpin up"
    exit 1
else
    echo "Azure tests succeed on linchpin up"
fi

linchpin -vvvv destroy;
if [ $? -ne 0 ]
then
    echo failed
    echo "Azure tests failed on linchpin destroy"
    exit 1
else
    echo "Azure tests succeed on linchpin up"
    
fi
