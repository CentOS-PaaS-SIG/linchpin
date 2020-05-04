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

echo "RUNNING AWS MOCK TESTS";

linchpin init aws;
cd aws;
linchpin -vvvv up aws-ec2-new;
linchpin -vvvv destroy aws-ec2-new;

linchpin -vvvv up aws-ec2-new;
linchpin -vvvv destroy aws-ec2-new;

linchpin -vvvv up aws-ec2-key-new;
linchpin -vvvv destroy aws-ec2--key-new;

linchpin -vvvv up aws-sg-new;
linchpin -vvvv destroy aws-sg-new;

linchpin -vvvv up aws-s3-new;
linchpin -vvvv destroy aws-s3-new;

linchpin -vvvv up aws-ec2-eip;
linchpin -vvvv destroy aws-ec2-eip;

linchpin -vvvv up aws-ec2-vpc-net;
linchpin -vvvv destroy aws-ec2-vpc-net;

linchpin -vvvv up aws-ec2-vpc-subnet;
linchpin -vvvv destroy aws-ec2-vpc-subnet;

linchpin -vvvv up aws-ec2-vpc-routetable;
linchpin -vvvv destroy aws-ec2-vpc-routetable;


linchpin -vvvv up aws-ec2-elb-lb;
linchpin -vvvv destroy aws-ec2-elb-lb;


linchpin -vvvv up aws-ec2-template;
linchpin -vvvv destroy aws-ec2-template;







