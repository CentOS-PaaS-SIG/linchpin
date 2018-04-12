#!/bin/bash -x

base_dir="$( pwd )"

set -o pipefail

mkdir -p ${base_dir}/${target}_logs

result=0
for i in $DRIVERS; do
    testname="$target/$i"
    export CREDS_PATH="$base_dir/keys/$i"
    # If CREDS_PATH provides a tarball extract it and
    # run it's install script
    if [ -e "$CREDS_PATH/${i}.tgz" ]; then
        tmpdir=$(mktemp -d)
        tar xvf $CREDS_PATH/${i}.tgz -C $tmpdir
        $tmpdir/install.sh
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
