#!/bin/bash
for var in "$@"
do
  eval "$var"
done
pip install testinfra
py.test --connection=ansible --hosts=example --ansible-inventory=$inventory_file
