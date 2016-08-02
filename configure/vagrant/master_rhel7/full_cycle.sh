#!/bin/bash

source ../shared.sh
vagrant_cycle master_rhel7 || exit 1
venv || exit 1
playbook master_rhel7 "$@" || exit 1
