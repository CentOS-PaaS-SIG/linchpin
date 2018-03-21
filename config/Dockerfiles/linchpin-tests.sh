#!/bin/bash

base_dir="$( pwd )"

set -o pipefail

mkdir -p ${base_dir}/${target}_logs

result=0
for i in $DRIVERS; do
    testname="$target/$i"
    export CREDS_PATH="$base_dir/keys/$i"
    # Horrible hacks until CentOS support is fixed..
    # See Issue: https://github.com/CentOS-PaaS-SIG/duffy-ansible-module/issues/3
    if [ "$target" = "centos6" -o "$target" = "centos7" ] && \
       [ "$i" = "aws-ec2-new" ]; then
        test_summary="$(tput setaf 4)SKIPPED$(tput sgr0)\t${testname}"
        summary="${summary}\n${test_summary}"
        continue
    fi
    if [ "$target" = "centos6" -a "$i" = "duffy" ]; then
        test_summary="$(tput setaf 4)SKIPPED$(tput sgr0)\t${testname}"
        summary="${summary}\n${test_summary}"
        continue
    fi
    ./config/Dockerfiles/linchpin-test.sh $i 2>&1 |tee ${target}_logs/${i}.log
    if [ $? -eq 0 ]; then
        test_summary="$(tput setaf 2)SUCCESS$(tput sgr0)\t${testname}"
    else
        test_summary="$(tput setaf 1)FAILURE$(tput sgr0)\t${testname}\tlog: logs/${target}_${i}.log"
        result=1
    fi
    summary="${summary}\n${test_summary}"
done

printf "\n==== TEST summary ====${summary}\n"
exit $result
