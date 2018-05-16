#!/bin/bash -x

base_dir="${PWD}"

set -o pipefail

mkdir -p ${base_dir}/${distro}_logs

TEST_DIR="./config/Dockerfiles/tests.d"

if [ -z "${PROVIDERS}" ]; then
    PROVIDERS="dummy libvirt"
fi

echo "Testing providers: ${PROVIDERS}"

summary=''
result=0
for provider in $PROVIDERS; do
    export CREDS_PATH="$base_dir/keys/${provider}"
    # If CREDS_PATH provides a tarball extract it and
    # run it's install script
    if [ -e "$CREDS_PATH/${provider}.tgz" ]; then
        tmpdir=$(mktemp -d)
        tar xvf $CREDS_PATH/${provider}.tgz -C $tmpdir
        $tmpdir/install.sh
    fi
    > ${distro}_logs/${provider}.log

    # run generic tests by passing in the provider and distro
    # should be enough to test the 'basic' provision/teardown


    for testfile in ${TEST_DIR}/general/*; do
        filename=$(basename -- "$testfile")
        test="general/${filename%.*}"
        testname=${distro}/${test}

        ignore=''
        if [ -e "${TEST_DIR}/${distro}-${provider}.ignore" ]; then
            ignore=$(grep ${test} ${TEST_DIR}/${distro}-${provider}.ignore | grep -v '^#')
        fi

        if [ -z "${ignore}" ]; then
            ${TEST_DIR}/general/${filename} ${distro} ${provider} 2>&1 | tee -a ${base_dir}/${distro}_logs/${provider}.log
            if [ $? -eq 0 ]; then
                test_summary="$(tput setaf 2)SUCCESS$(tput sgr0)\t${testname}"
            else
                test_summary="$(tput setaf 1)FAILURE$(tput sgr0)\t${testname}\tlog: logs/${distro}_logs/_${provider}.log"
                result=1
            fi
            summary="${summary}\n${test_summary}"
        fi
    done

    if [ -d "${TEST_DIR}/${provider}" ]; then
        for testfile in ${TEST_DIR}/${provider}/*; do
            filename=$(basename -- "$testfile")
            test="${filename%.*}"

            ignore=''
            if [ -e "${TEST_DIR}/${distro}-${provider}.ignore" ]; then
                ignore=$(grep ${test} ${TEST_DIR}/${distro}-${provider}.ignore | grep -v '^#')
            fi

            if [ -z "${ignore}" ]; then
                testname="${distro}/${provider}/${test}"
                ${TEST_DIR}/${provider}/${test} ${distro} ${provider} 2>&1 | tee -a ${base_dir}/${distro}_logs/${provider}.log
                if [ $? -eq 0 ]; then
                    test_summary="$(tput setaf 2)SUCCESS$(tput sgr0)\t${testname}"
                else
                    test_summary="$(tput setaf 1)FAILURE$(tput sgr0)\t${testname}\tlog: logs/${distro}_logs/_${provider}.log"
                    result=1
                fi
                summary="${summary}\n${test_summary}"
            fi
        done
    fi
done

printf "\n==== TEST summary ====${summary}\n"
exit $result
