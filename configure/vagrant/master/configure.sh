#!/bin/bash

source ../shared.sh

venv || exit 1

playbook master "$@" || exit 1
