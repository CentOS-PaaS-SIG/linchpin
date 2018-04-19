#!/bin/bash

set -o pipefail

LINCHPINDIR=$1
shift
DISTROS=$*
TARGETS="dummy"

export WORKSPACE="/tmp"

# Pull down duffy-ansible-module
if [ -d "duffy-ansible-module" ]; then
    pushd duffy-ansible-module && git pull
    popd
else
    git clone https://github.com/CentOS-PaaS-SIG/duffy-ansible-module.git
fi

for distro in $DISTROS; do
    container="lp_$distro"
    docker run --privileged -d -v $LINCHPINDIR:/workdir/ \
        -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name $container $container
done

for distro in $DISTROS; do
    container="lp_$distro"
    docker exec -it $container bash -c 'pushd /workdir && ./config/Dockerfiles/linchpin-install.sh'
    docker exec -it $container bash -c "export distro=$distro; export TARGETS=\"$TARGETS\"; pushd /workdir && ./config/Dockerfiles/linchpin-tests.sh"
done

for distro in $DISTROS; do
    container="lp_$distro"
    docker kill $container
    docker rm $container
done
