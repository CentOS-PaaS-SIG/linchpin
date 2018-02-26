#!/bin/bash

set -o pipefail

LINCHPINDIR=$1
shift
TARGETS=$*
DRIVERS="dummy"

export WORKSPACE="/tmp"

# NOTE: this is replaced by workdir/docs/source/examples/workspace
# in the linchpin repo
# Pull latest example topologies
#if [ -d "lp_test_workspace" ]; then
#    pushd lp_test_workspace && git pull
#    popd
#else
#    git clone https://github.com/herlo/lp_test_workspace.git
#fi

# Pull down duffy-ansible-module
if [ -d "duffy-ansible-module" ]; then
    pushd duffy-ansible-module && git pull
    popd
else
    git clone https://github.com/CentOS-PaaS-SIG/duffy-ansible-module.git
fi

for target in $TARGETS; do
    container="lp_$target"
    docker run --privileged -d -v $LINCHPINDIR:/workdir/ \
        -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name $container $container
done

mkdir -p logs
for target in $TARGETS; do
    container="lp_$target"
    docker exec -it $container bash -c 'pushd /workdir && ./config/Dockerfiles/linchpin-install.sh'
    for i in $DRIVERS; do
        testname="$target/$i"
        if [ "$i" = "duffy" -a ! -e "duffy.key" ]; then
            test_summary="$(tput setaf 4)SKIPPED$(tput sgr0)\t${testname}"
            summary="${summary}\n${test_summary}"
            continue
        fi
        docker exec -it $container bash -c "pushd /workdir && ./config/Dockerfiles/linchpin-test.sh $i" 2>&1 |tee logs/${target}_${i}.log
        if [ $? -eq 0 ]; then
            test_summary="$(tput setaf 2)SUCCESS$(tput sgr0)\t${testname}"
        else
            test_summary="$(tput setaf 1)FAILURE$(tput sgr0)\t${testname}\tlog: ./logs/${target}_${i}.log"
            result=1
        fi
        summary="${summary}\n${test_summary}"
    done
done

for target in $TARGETS; do
    container="lp_$target"
    docker kill $container
    docker rm $container
done

printf "\n==== TEST summary ====${summary}\n"
