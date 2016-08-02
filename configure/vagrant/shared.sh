#!/bin/bash

set -x

TOP=$(readlink -f "$(dirname "${0}")/../../../")

function venv {
    /bin/bash "${TOP}/bin/ensure_virtualenv.sh" || exit 1
}

function playbook {
    source "${TOP}/.venv/bin/activate"
    directory="${1}"
    shift
    ansible-playbook -i "${TOP}/configure/vagrant/${directory}/hosts" "${TOP}/configure/site.yml" \
        -e "vagrant_dir=${TOP}/configure/vagrant/${directory}" \
        "$@" || exit 1
    deactivate
}

function vagrant_cycle {
    cd "${TOP}/configure/vagrant/${1}/"
    vagrant destroy -f || exit 1
    vagrant up || exit 1
}
