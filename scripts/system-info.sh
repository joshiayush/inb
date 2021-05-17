#!/bin/bash

function getSystemInfo() {
    # Function that finds the system platform Information.
    case "$(/usr/bin/lsb_release -si)" in
    Ubuntu) echo "Ubuntu" ;;
    Mint) echo "Mint" ;;
    arch) echo "Arch" ;;
    *) echo "Can not get the System Information! Download Python manually" ;;
    esac
}
