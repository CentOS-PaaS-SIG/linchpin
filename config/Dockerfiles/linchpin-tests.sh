#!/bin/bash

base_dir="$( pwd )"

set -o pipefail

mkdir -p ${base_dir}/logs

result=0
for i in $DRIVERS; do
    testname="$target/$i"
    if [ "$i" = "duffy" -a ! -e "duffy.key" ]; then
        test_summary="$(tput setaf 4)SKIPPED$(tput sgr0)\t${testname}"
        summary="${summary}\n${test_summary}"
        continue
    fi
    /root/linchpin-test.sh $i 2>&1 |tee logs/${target}_${i}.log
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
