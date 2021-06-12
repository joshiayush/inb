#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Root permissions required!"
  exit
fi

declare -a garbages=("__pycache__/"
  "linkedin-bot/__pycache__/"
  "linkedin-bot/DOM/__pycache__/"
  "linkedin-bot/user/__pycache__/"
  "linkedin-bot/goto/__pycache__/"
  "linkedin-bot/tests/__pycache__/"
  "linkedin-bot/creds/__pycache__/"
  "linkedin-bot/errors/__pycache__/"
  "linkedin-bot/helpers/__pycache__/"
  "linkedin-bot/console/__pycache__/"
  "linkedin-bot/linkedin/__pycache__/"
  "linkedin-bot/database/__pycache__/"
  "linkedin-bot/messages/__pycache__/"
  "linkedin-bot/invitation/__pycache__/"
  "linkedin-bot/javascript/__pycache__/")

for garbage in "${garbages[@]}"; do
  if [ -d "${garbage}" ]; then
    sudo rm -rf "${garbage}"
    echo "${garbage} directory is present, deleted ..." 
  else
    echo "${garbage} directory is not present, skipping ..."
  fi
done
