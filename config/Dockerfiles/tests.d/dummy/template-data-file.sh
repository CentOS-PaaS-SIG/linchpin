#!/bin/bash -xe

DISTRO=${1}
PROVIDER=${2}

function clean_up {
    set +e
    linchpin -w . -p PinFile.${PROVIDER}.yml --template-data @./dummy-data.yml -v destroy dummy-new
}
trap clean_up EXIT SIGHUP SIGINT SIGTERM

pushd docs/source/examples/workspace
cat << EOF > dummy-data.yml
---
distro: "${DISTRO}-"
EOF

cat dummy-data.yml

if [ -e /tmp/dummy.hosts ]; then
    rm /tmp/dummy.hosts
fi

linchpin -w . -p PinFile.${PROVIDER}.yml --template-data @dummy-data.yml -v up dummy-new

grep "${DISTRO}" /tmp/dummy.hosts

