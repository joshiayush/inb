#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Root permissions required!"
  exit
fi

function installOnUbuntu() {
  # Function that install python and selenium on Ubuntu platform.
  if ls /usr/bin | grep python3.8 > /dev/null; then
    echo "python3.7 is already installed, skipping ..."
  else
    printf "[%(%Y-%m-%d %H:%M:%S)T] Installing python3.7 on Ubuntu Linux ...\n" -7
    sudo apt-get update
    sudo apt-get install python3.7 python3-pip
  fi
}

function installOnMint() {
  # Function that install python and selenium on Linux Mint platform. On Linux Mint we first need to add a personal package
  # archive i/e., 'ppa:deadsnakes/ppa' to install python.
  if ls /usr/bin | grep python3.7 > /dev/null; then
    echo "python3.7 is already installed, skipping ..."
  else
    printf "[%(%Y-%m-%d %H:%M:%S)T] Installing python3.7 on Linux Mint ...\n" -1
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.7 python3-pip
  fi
}

function installOnArch() {
  # Function that install python and selenium on Arch Linux platform using `packman`.
  if ls /usr/bin | grep python3.7 > /dev/null; then
    echo "python3.7 is already installed, skipping ..."
  else
   printf "[%(%Y-%m-%d %H:%M:%S)T] Installing python3.7 on Arch Linux ...\n" -1
   packman -S python
  fi
}
        
source /Python/linkedin-bot/scripts/system-info.sh

echo "Installing python for $(uname -s) ..."

case "$(getSystemInfo)" in
  Ubuntu) installOnUbuntu ;;
  Mint) installOnMint ;;
  Arch) installOnArch ;;
  *) 
    echo "Cannot find system information! Download python manually!"
    echo "You can submit an issue related to this problem at https://github.com/JoshiAyush/linkedin-bot/issues"
    exit 
  ;;
esac

sudo ./scripts/install-dependencies.sh 