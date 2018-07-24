#!/bin/bash -xe

TARGET=${1}
DISTRO=${2}

function clean_up {
    set +e
    linchpin -w . -v --template-data "{\"distro\": \"${DISTRO}-\"}" destroy ${TARGET}
}
trap clean_up EXIT SIGHUP SIGINT SIGTERM

pushd docs/source/examples/workspace
echo "DISTRO: ${DISTRO}"
linchpin -w . -v --template-data "{\"distro\": \"${DISTRO}-\"}" up ${TARGET}
