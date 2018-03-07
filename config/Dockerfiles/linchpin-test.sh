#!/bin/bash -xe

DRIVER=$1

function clean_up {
    set +e
    linchpin -w . -v destroy $DRIVER
}
trap clean_up EXIT SIGHUP SIGINT SIGTERM

pushd docs/source/examples/workspace
linchpin -w . -v up $DRIVER
