#!/bin/bash

if [ "$EUID" -eq 0 ]; then
  echo "Run this script as normal user!"
  exit
fi

if python3.7 --version | grep "Python*" >/dev/null; then
  echo "python3.7 is installed, running program inb/main.py ..."
  python3.7 inb/main.py
else
  echo "python3.7 is not installed, please install it first!"
fi
