#!/bin/bash

source ../shared.sh

vagrant_cycle master || exit 1

venv || exit 1

playbook master "$@" || exit 1
