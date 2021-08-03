#!/bin/bash

function installPackages() {
  local readonly verbose=$1

  if [ -f "$ProjectRootDirectory/requirements.txt" -o -s "$ProjectRootDirectory/requirements.txt" ]; then
    if [ $verbose -eq 0 ]; then
      python3 -m pip install -r requirements.txt
    else
      python3 -m pip install -r requirements.txt >/dev/null
    fi
  fi
}
