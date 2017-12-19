#!/bin/bash -xe

DRIVER=$1

function clean_up {
    set +e
    linchpin -v destroy $DRIVER
}
trap clean_up EXIT SIGHUP SIGINT SIGTERM

pushd /workdir/docs/source/examples/workspace
linchpin -v up $DRIVER
