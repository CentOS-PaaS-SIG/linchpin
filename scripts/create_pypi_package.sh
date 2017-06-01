#!/bin/bash

if [ $# -lt 2 ]; then
  PYPI=pypitest
else
  PYPI=${2}
fi

if [ $# -lt 1 ]; then
  echo "Usage $0 <lp-path> <pypi-site>"
  echo
  echo lp-path: path to linchpin source
  echo pypi-site: path to linchpin source
  exit 1
fi

PROMPT=1

PKG_TYPES="sdist bdist_wheel"
SETUP_CMD="python setup.py"
CLEAN_CMD="clean"
REG_CMD="register"
UPLOAD_CMD="upload ${PKG_TYPES}"

# find extraneous files and remove them
CRUFTIES=('coverage.xml' 'linchpin.log')

echo "REMOVING CRUFTY FILES"

for CRUFT in "${CRUFTIES[@]}"; do
    echo "find -name ${CRUFT} -delete"
done

CLEAN="${SETUP_CMD} ${CLEAN_CMD}"
REG="${SETUP_CMD} ${REG_CMD} -r ${PYPI}"
UPLOAD="${SETUP_CMD} ${UPLOAD_CMD} -r ${PYPI}"

for ACTION in "${CLEAN}" "${REG}" "${UPLOAD}"; do
    if [ ${PROMPT} -eq 1 ]; then
        read -p "Run ${ACTION} ([Y]/n)? " yn
        case $yn in
            [Yy]* ) echo "RUNNING ${ACTION}"; ${ACTION};;
            [Nn]* ) echo "EXITING"; exit;;
            * ) echo "RUNNING ${ACTION}"; ${ACTION};;
        esac
    else
        echo "RUNNING ${ACTION}"
        ${ACTION}
    fi
done


#echo ${REG_CMD}
#
#echo ${UPLOAD_CMD}
