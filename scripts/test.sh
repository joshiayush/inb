#!/bin/bash

if [ "$EUID" -eq 0 ]; then
  echo "Run this script as normal user!"
  exit
fi

python3.7 linkedin-bot/test.py

sudo ./scripts/delete-garbage.sh