#!/bin/bash -xe

DISTRO=${1}
PROVIDER=${2}

function clean_up {
    set +e
    linchpin -w . -p PinFile.dummy.yml --template-data "{\"distro\": \"${DISTRO}-\"}" -v destroy dummy-new
}
trap clean_up EXIT SIGHUP SIGINT SIGTERM

if [ -e /tmp/dummy.hosts ]; then
    rm /tmp/dummy.hosts
fi

pushd docs/source/examples/workspace

linchpin -w . -p PinFile.dummy.yml --template-data "{\"distro\": \"${DISTRO}-\"}" -v up dummy-new

grep "${DISTRO}" /tmp/dummy.hosts

