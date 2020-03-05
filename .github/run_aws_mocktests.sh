#!/usr/bin/env bash
echo "Hello this is first attempt to run linchpin provisioning in github actions"


VERSION_ID=$(cat /etc/*release | grep ^VERSION_ID | tr -d 'VERSION_ID="')

echo $VERSION_ID

if [ $VERSION_ID = "7" ]
then
    echo "This is centos7";
    export LC_ALL="en_US";
    export LANG="en_US";
fi


linchpin --version;

mkdir /tmp/workspace/;

cd /tmp/workspace/;

echo $PWD;

locale -a;

echo $LC_ALL;
export $LANG;

echo "RUNNING AWS MOCK TESTS";

linchpin init aws;
cd aws;
linchpin -vvvv up;
linchpin -vvvv destroy;
