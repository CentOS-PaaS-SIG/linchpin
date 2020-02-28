#!/bin/bash -x

base_dir="${PWD}"

set -o pipefail

mkdir -p ${base_dir}/${distro}_logs
rm -f ${base_dir}/${distro}_logs/*

TESTS_DIR="./config/Dockerfiles/tests.d"


# this function checks the distros.exclude value within the test.
# If none, false is returned and the disro hasn't been excluded.
# If distros.exclude includes a distro name, it is chedked against
# the ${distro} env var. If they match true is sent back to the caller
# and the test will be skipped for that distro.
function check_distro_exclude () {
    shopt -s extglob
    test=${1}
    dist_exc=$(grep '^#.*distros.exclude' ${test} | grep -v 'none' | awk -F':' '{ print $2 }')

    # if distros.exclude matches the ${distro} env var, return true
    if [ ! -z "${dist_exc}" ]; then
        for d in ${dist_exc}; do
            d="${d##+([[:space:]])}"
            if [ "${distro}" == "${d}" ]; then
                echo 1
                return
            fi
        done
    fi
    shopt -u extglob
}

providers=''
# this function checks the test and returns valid providers
# then compares them to the ${PROVIDERS} var and returns
# matches
function set_providers () {
    shopt -s extglob
    test=${1}

    prov_inc=$(grep '^#.*providers.include' ${test} | grep -v 'none' | awk -F':' '{ print $2 }')
    if [ ! -z "${prov_inc}" ]; then
        providers=''
        for p in ${prov_inc}; do
            p="${p##+([[:space:]])}"
            for pr in ${PROVIDERS}; do
                if [ "${p}" == "${pr}" ]; then
                    providers="${providers} ${p}"
                fi
            done
        done
    fi

    # provider.excludes only gets tested if there are no providers.includes set
    prov_exc=''
    if [ -z "${prov_inc}" ]; then
        providers=${PROVIDERS}
	prov_exc=$(grep '^#.*providers.exclude' ${test} | grep -v 'none' | awk -F':' '{ print $2 }'; echo "__RELEASE__")
        if [ ! -z "${prov_exc}" ]; then
             for p in ${prov_exc}; do
                 p="${p##+([[:space:]])}"
                 providers="${providers//${p}/}"
            done
        fi
    fi

    providers="${providers##+([[:space:]])}"
    shopt -u extglob
}



summary=''
result=0
#

export CREDS_PATH="$base_dir/keys"
pushd "${CREDS_PATH}"

for provider in ${PROVIDERS}; do
    # If CREDS_PATH provides a tarball extract it and
    # run it's install script
    if [ -e "$CREDS_PATH/${provider}.tgz" ]; then
        tmpdir=$(mktemp -d)
        tar xvf $CREDS_PATH/${provider}.tgz -C $tmpdir
        $tmpdir/install.sh
    fi
done
popd

#    # run generic tests by passing in the provider and distro
#    # should be enough to test the 'basic' provision/teardown

pushd "${TESTS_DIR}" &> /dev/null
for testdir in *; do
    if [ -n "$(ls ${testdir})" ]; then
        pushd "${testdir}" &> /dev/null
        for test in *; do
            echo
            if [ ! $(check_distro_exclude "${test}") ]; then
                set_providers "${test}"
                for provider in ${providers}; do

                    tname="${provider}/${test}"
                    testname=${distro}/${tname}
                    echo >> ${base_dir}/${distro}_logs/${provider}.log
                    echo "==== TEST: ${testname} ====" | tee -a ${base_dir}/${distro}_logs/${provider}.log
                    pushd "${base_dir}" &> /dev/null
                    ${TESTS_DIR}/${testdir}/${test} ${distro} ${provider} ${CREDS_PATH} 2>&1 | tee -a ${base_dir}/${distro}_logs/${provider}.log
                    RC=${?}
                    if [ ${RC} -eq 0 ]; then
                        test_summary="$(tput setaf 2)SUCCESS$(tput sgr0)\t${testname}"
                    else
                        test_summary="$(tput setaf 1)FAILURE$(tput sgr0)\t${testname}\tlog: ${distro}_logs/${provider}.log"
                        result=1
                    fi
                    summary="${summary}\n${test_summary}"
                    echo >> ${base_dir}/${distro}_logs/${provider}.log
                    popd &> /dev/null

                done
            fi
        done
        popd &> /dev/null
    fi
done
popd &> /dev/null

printf "\n==== TEST summary ====${summary}\n"
exit $result
