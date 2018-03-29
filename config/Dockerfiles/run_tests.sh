#!/bin/bash

set -o pipefail

LINCHPINDIR=$1
shift
TARGETS=$*
DRIVERS="dummy"

export WORKSPACE="/tmp"

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
