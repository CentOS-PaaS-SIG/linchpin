#!/bin/bash -xe

DRIVER=$1

pushd /workdir/Dockerfiles/lp_test_workspace
linchpin up $DRIVER
