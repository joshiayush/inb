#!/bin/bash

if [ "$EUID" -eq 0 ]; then
  echo "Run this script as a normal user!"
  exit
fi

echo "Installing ..."
python3 -m pip install -r requirements.txt 
