#!/bin/bash
# Use this script to run the Jenkins configuration against the inventory under
# configure/inventory/local. See the docs for more information about the proper
# way to setup that inventory folder

TOP=$(dirname $(readlink -f $(dirname $0)))

/bin/bash "${TOP}/bin/ensure_virtualenv.sh"
source "${TOP}/.venv/bin/activate"

ansible-playbook -i "${TOP}/configure/inventory/local/hosts" "${TOP}/configure/site.yml" "$@"

ANSIBLE_EXIT=$?

# Teardown the virtualenv so we don't leave anything floating
deactivate

exit ${ANSIBLE_EXIT}
