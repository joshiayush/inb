#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Root permissions required!"
  exit
fi

declare -a build_dirs=("build"
  "dist")

declare -a build_files=("main.spec")

echo "Deleting builds ..."

for dir in "${build_dirs[@]}"; do
  echo "Deleting ${dir} directory ..."
  sudo rm -rf dir
done


for file in "${build_files[@]}"; do
  echo "Deleting ${file} file ..."
  sudo rm file
done