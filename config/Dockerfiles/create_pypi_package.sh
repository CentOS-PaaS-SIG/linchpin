#!/bin/bash

if [ $# -lt 2 ]; then
  PYPI=pypitest
else
  PYPI=${2}
fi

if [ $# -lt 1 ]; then
  echo "Usage $0 <tag> [<pypi-site>]"
  echo
  echo "tag: version tag (eg. v1.5.3)"
  echo "pypi-site: path to linchpin source (default: pypitest)"
  exit 1
fi

GIT_TAG=${1}
PROMPT=1

PKG_TYPES="sdist bdist_wheel"
SETUP_CMD="python setup.py"
CLEAN_CMD="clean"
UPLOAD_CMD="${PKG_TYPES} upload"
GIT=$(which git)

#TMP_DIR=$(mktemp -d)

CLEAN="${SETUP_CMD} ${CLEAN_CMD}"
UPLOAD="${SETUP_CMD} ${UPLOAD_CMD} -r ${PYPI}"

#${GIT} clone ${LP_GIT_URL} ${TMP_DIR}
#pushd ${TMP_DIR}
#${GIT} fetch --all --tags --prune
#${GIT} checkout tags/${GIT_TAG} -b lp_${GIT_TAG}

#if [ "$?" != "0" ]; then
#    echo "Tag could not be checked out, verify tag is in git and try again"
#    exit 2
#fi

for ACTION in "${CLEAN}" "${UPLOAD}"; do
#    if [ ${PROMPT} -eq 1 ]; then
#        echo
#        read -p "Run ${ACTION} ([Y]/n)? " yn
#        case $yn in
#            [Yy]* ) echo "RUNNING ${ACTION}"; ${ACTION};;
#            [Nn]* ) echo "EXITING"; exit;;
#            * ) echo "RUNNING ${ACTION}"; ${ACTION};;
#        esac
#    else
    echo "RUNNING ${ACTION}"
    echo ${ACTION}
#    fi
done

#popd

