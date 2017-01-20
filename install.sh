#!/bin/bash

for line in $(cat requirements.txt)
do
  pip install $line
  if [ $? != 0 ]; then
    echo "Failed install of pip module $line"
    exit 1;
  fi
done