#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Root permissions required!"
  exit
fi

declare -a garbages=("__pycache__/"
  "inb/__pycache__/"
  "inb/lib/__pycache__/"
  "inb/DOM/__pycache__/"
  "inb/user/__pycache__/"
  "inb/goto/__pycache__/"
  "inb/tests/__pycache__/"
  "inb/creds/__pycache__/"
  "inb/errors/__pycache__/"
  "inb/helpers/__pycache__/"
  "inb/console/__pycache__/"
  "inb/linkedin/__pycache__/"
  "inb/database/__pycache__/"
  "inb/messages/__pycache__/"
  "inb/invitation/__pycache__/"
  "inb/javascript/__pycache__/"
  "inb/database/sql/__pycache__/"
  "inb/tests/console/__pycache__/"
  "inb/helpers/parser/__pycache__/"
  "inb/tests/linkedin/__pycache__/"
  "inb/database/firebase/__pycache__/")

for garbage in "${garbages[@]}"; do
  if [ -d "${garbage}" ]; then
    sudo rm -rf "${garbage}"
    echo "${garbage} directory is present, deleted ..." 
  else
    echo "${garbage} directory is not present, skipping ..."
  fi
done
