#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Root permissions required!"
  exit
fi

declare -a packages=("selenium"
  "webdriver-manager")

echo "Installing dependencies..."

for package in "${packages[@]}"; do
  if pip3 list | grep "${package}" > /dev/null; then
    echo "${package} is installed, skipping ..."
  else
    printf "[%(%Y-%m-%d %H:%M:%S)T] Installing ${package} ...\n" -1
    sudo pip3 install "${package}"
  fi
done
