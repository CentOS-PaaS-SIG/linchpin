#!/bin/bash

source ../shared.sh
venv || exit 1
playbook master_rhel7 "$@" || exit 1
