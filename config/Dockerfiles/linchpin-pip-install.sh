#!/bin/bash -x

# This script installs linchpin from test.pypi.org
# used by cd-linchpin-release (JenkinsfileRelease)
# will only be used on the latest distro (currently
# fedora29 and the dummy provider).

VERSION=${1}
TMPDIR=$(mktemp -d)

PYPI=https://test.pypi.org/simple

#pip3 install -U pip setuptools

# wait for test.pypi.org to have files
sleep 10

pip3 download linchpin==${VERSION} --index-url ${PYPI} --retries 10 --pre --no-deps --no-binary :all: -d ${TMPDIR}

# grab the requirements.txt from the linchpin package and intall those packages from production pypi
tar -xvf ${TMPDIR}/linchpin-${VERSION}.tar.gz -C ${TMPDIR} linchpin-${VERSION}/requirements.txt --strip-components=1
pip3 install -r ${TMPDIR}/requirements.txt

# once deps are installed from production pypi, install linchpin from test.pypi
pip3 install linchpin==${VERSION} --index-url ${PYPI}

# verify linchpin is installed
linchpin --version 2>&1 | grep ${VERSION}
if [ "${?}" -eq "0" ]; then
    echo SUCCESS
    exit 0
fi
echo FAILURE
exit 1

