#!/bin/bash

# * The line at the head of the script tells the shell that it is a shell
# * script and it contains commands in it and you need to execute it
# ? #!/bin/sh
# * Executes the script using the Bourne shell or a compatible shell, with path /bin/sh
# ? #!/bin/bash
# * Executes the script using the Bash shell.
# ? #!/bin/csh -f
# * Executes the script using C shell or a compatible shell.
# ? #!/usr/bin/perl -T
# * Executes the script using perl with the option of taint checks
# ? #!/usr/bin/env python
# * Executes the script using python by looking up the path to the python interpreter automatically
# * from the environment variables

# * Shell is an interface using which the programmer can execute command
# * and interact directly to the operating system. Shell scripting is
# * giving commands that a shell can execute.

# ? here the program start its execution
# ? `$1` is the first argument of the function
# ? `runProgram` and its value is the python
# ? interpreter i.e., python[2/3], we check the
# ? system here because Windows uses '\' for navigation
# ? and Linux '/'
function runProgram() {
    if [ "$2" = "linux" ]; then
        $1 src/main.py
    elif [ "$2" = "windows" ]; then
        $1 src\main.py
    else
        echo "System not identified"
    fi
}

# ! function to confirm the user decision of Installing
# ! python if it is not installed
function confirm() {
    read -p "Install Python [y/n]: " ch
    echo $ch
}

# ! function that finds the system platform Information
function getSystemInfo() {
    case "$(/usr/bin/lsb_release -si)" in
    Ubuntu) echo "Ubuntu" ;;
    Mint) echo "Mint" ;;
    arch) echo "Arch" ;;
    *) echo "Can not get the System Information! Download Python manually" ;;
    esac
}

# ! function that install python on Ubuntu platform
function installOnUbuntu() {
    echo "Installing Python on Ubuntu Linux"
    sudo apt-get update
    sudo apt-get install python3.8 python3-pip
}

# ! function that install python on Linux Mint platform
function installOnMint() {
    echo "Installing Python on Linux Mint"
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.8 python3-pip
}

# ! function that install python on Arch Linux platform
function installOnArch() {
    echo "Installing Python on Arch Linux"
    packman -S python
}

# ! function that install python in Windows using Microsoft
# ! installer
function installOnWindows() {
    msiexec /i python-3.8.msi TARGETDIR=C:\Python
}

# ? function that install python on OSX system
# ?
# ! To install python on OSX we first need to install Apple’s Xcode
# ! program which is necessary for iOS development as well as most
# ! programming tasks,
# ! then we need to install homebrew utility,
# ! then we can install python
function installOnOSX() {
    # ! install xcode
    xcode-select --install
    # ! install homebrew utility
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    # ! install python3
    brew install python3
}

# ? function that returns the name of the operating system that the
# ? user is running in its system variable OSTYPE is a predefined
# ? variable that stores the name of the Operating System that is
# ? running currently
function getOsInfo() {
    echo $OSTYPE
}

# ? function that does the actual installation of the python interpreter
# ? based on the current running platform
function install() {
    case "$(getOsInfo)" in
    linux*)
        # * install python based on the running platform
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

# ? function that install python if it is not already installed
# ? in the user system
function installPython() {
    # ! get confirmation
    ch=$(confirm)

    if [ "$ch" = "y" ]; then
        echo "Installing python for $(uname -s)"
        install
    else
        echo "Piece"
    fi
}

# ? function main is the main function that starts the execution of the
# ? linkedin automator program it first checks if the requirements are
# ? present or not then it takes actions accordingly
function main() {
    # ! check if python3 is present, /dev/null makes the grep output disappear
    if python3 --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        runProgram python3 "linux"
    # ! check if python2 is present, /dev/null makes the grep output disappear
    elif python2 --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        runProgram python2 "linux"
    # ! check if python is present, /dev/null makes the grep output disappear
    elif python --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        runProgram python "linux"
    # ! check if python is present command 'py' is for windows, /dev/null makes the grep output disappear
    elif py --version | grep "Python*"; then
        echo "Python is installed"
        runProgram py "windows"
    # ! install python if python is not present
    else
        echo "Python is not installed"
        installPython
    fi
}

# ! start
main
