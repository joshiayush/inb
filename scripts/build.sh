#!/bin/bash

if [ "$EUID" -eq 0 ]; then
  echo "Run this script as a normal user!"
  exit
fi

echo "Building linkedin-bot ..."
/usr/bin/python3.7 -m PyInstaller ./inb/main.py

echo "Executing binary file main ..."
./dist/main/main   