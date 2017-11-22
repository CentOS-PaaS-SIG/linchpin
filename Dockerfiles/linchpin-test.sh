#!/bin/bash -xe

DRIVER=$1

function clean_up {
    set +e
    linchpin -v down $DRIVER
}
trap clean_up EXIT SIGHUP SIGINT SIGTERM

pushd /workdir/Dockerfiles/lp_test_workspace
linchpin -v up $DRIVER
