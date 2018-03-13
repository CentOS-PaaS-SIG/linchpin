#!/bin/bash

set -o pipefail

LINCHPINDIR=$1
shift
TARGETS=$*
DRIVERS="aws-ec2-new duffy dummy"

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
    docker exec -it $container bash -c "export target=$target; export DRIVERS=\"$DRIVERS\"; pushd /workdir && ./config/Dockerfiles/linchpin-tests.sh"
done

for target in $TARGETS; do
    container="lp_$target"
    docker kill $container
    docker rm $container
done
