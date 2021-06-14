#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Root permissions required ..."
  exit
fi

echo "Changing $PWD directory permissions ..."

sudo chmod 777 -R $PWD

echo "Setting git config core.filemode to false to not to track file bits when not in the main system ..."
git config core.filemode false