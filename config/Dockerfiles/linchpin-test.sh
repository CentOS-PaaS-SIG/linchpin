#!/bin/bash -xe

TARGET=$1

function clean_up {
    set +e
    linchpin -w . -v destroy $TARGET
}
trap clean_up EXIT SIGHUP SIGINT SIGTERM

pushd docs/source/examples/workspace
linchpin -w . -v up $TARGET
