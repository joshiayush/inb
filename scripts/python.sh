#!/bin/bash

function installDependencies() {
    # Function to install the program dependencies like selenium module, webdriver-manager, urllib module.
    echo "Installing dependencies..."
    echo "Installing Selenium"
    pip3 install selenium
    echo "Installing WebDriver Manager"
    pip3 install webdriver-manager
}

function installOnUbuntu() {
    # Function that install python and selenium on Ubuntu platform.
    echo "Installing Python on Ubuntu Linux"
    sudo apt-get update
    sudo apt-get install python3.8 python3-pip
    installDependencies
}

function installOnMint() {
    # Function that install python and selenium on Linux Mint platform. On Linux Mint we first need to add a personal package
    # archive i/e., 'ppa:deadsnakes/ppa' to install python.
    echo "Installing Python on Linux Mint"
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.8 python3-pip
    installDependencies
}

function installOnArch() {
    # Function that install python and selenium on Arch Linux platform using `packman`.
    echo "Installing Python on Arch Linux"
    packman -S python
    installDependencies
}

function installOnWindows() {
    # Function that install python and selenium in Windows using Microsoft installer. We first install python using microsoft
    # installer then we move the installed file to `C:\` partition.
    msiexec /i python-3.8.msi TARGETDIR=C:\Python
    installDependencies
}

function installOnOSX() {
    # Function that install python on OSX system. To install python and selenium on OSX we first need to install Apple’s Xcode
    # program which is necessary for iOS development as well as most programming tasks, then we need to install homebrew utility
    # using `ruby`, then we can install python.
    xcode-select --install
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew install python3
    installDependencies
}

function install() {
    # Function that does the actual installation of the python interpreter based on the current running platform. In case of Linux
    # system we then further try to install python based on the platform.
    source /Python/linkedin-bot/scripts/os-type.sh

    case "$(getOsInfo)" in
    linux*)
        source /Python/linkedin-bot/scripts/system-info.sh
        case "$(getSystemInfo)" in
        Ubuntu) installOnUbuntu ;;
        Mint) installOnMint ;;
        Arch) installOnArch ;;
        *) exit ;;
        esac
        ;;
    msys*)
        installOnWindows
        ;;
    darwin*)
        installOnOSX
        ;;
    *) echo "System Information not found download Python Manually" ;;
    esac
}

function confirm() {
    # Function to confirm the user decision of Installing python if it is not installed.
    read -p "Install Python [y/n]: " ch
    echo $ch
}

function installPython() {
    # Function that install python if it is not already installed in the user system. This function first asks the user if (s)he
    # actually want to install python on his/her system then proceed accordingly.
    ch=$(confirm)

    if [ "$ch" = "y" ]; then
        echo "Installing python for $(uname -s)"
        install
    else
        echo "Piece"
    fi
}
