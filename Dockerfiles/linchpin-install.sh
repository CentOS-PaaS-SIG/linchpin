#!/bin/bash

pushd /workdir
pip install .
pip install .[tests]
pip install .[libvirt]
