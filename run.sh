#!/bin/bash

function runProgram() {
    # Here the program start its execution `$1` is the first argument of the function `runProgram` and its value is the python
    # interpreter i.e., python[2/3], we check the system here because Windows uses '\' for navigation and Linux '/'.
    if [ "$2" = "linux" ]; then
        $1 src/main.py
    elif [ "$2" = "windows" ]; then
        $1 src\main.py
    else
        echo "System not identified"
    fi
}

function confirm() {
    # Function to confirm the user decision of Installing python if it is not installed.
    read -p "Install Python [y/n]: " ch
    echo $ch
}

function getSystemInfo() {
    # Function that finds the system platform Information.
    case "$(/usr/bin/lsb_release -si)" in
    Ubuntu) echo "Ubuntu" ;;
    Mint) echo "Mint" ;;
    arch) echo "Arch" ;;
    *) echo "Can not get the System Information! Download Python manually" ;;
    esac
}

function installDependencies() {
    # Function to install the program dependencies like selenium module, webdriver-manager, urllib module.
    echo "Installing dependencies..."
    echo "Installing Selenium"
    pip3 install selenium
    echo "Installing URL handling python module (urllib)"
    pip3 install urllib3
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

function getOsInfo() {
    # Function that returns the name of the operating system that the user is running in its system, variable OSTYPE is a predefined
    # variable that stores the name of the Operating System that is running currently.
    echo $OSTYPE
}

function _echoInstallingPython() {
    echo "Installing Python ..."
    echo "Getting system info ..."
}

function install() {
    # Function that does the actual installation of the python interpreter based on the current running platform. In case of Linux
    # system we then further try to install python based on the platform.
    _echoInstallingPython
    case "$(getOsInfo)" in
    linux*)
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

function checkIfGarbage() {
    # Function checkIfGarbage() checks if the __pycache__ garbage is present, if yes then it returns a string 'yes' otherwise does
    # not return anything.
    declare -a garbages=("__pycache__+++"
        "src+++__pycache__+++"
        "src+++db+++__pycache__+++"
        "src+++dom+++__pycache__+++"
        "src+++creds+++__pycache__+++"
        "src+++errors+++__pycache__+++"
        "src+++helpers+++__pycache__+++"
        "src+++console+++__pycache__+++"
        "src+++linkedin+++__pycache__+++"
        "src+++invitation+++__pycache__+++"
        "src+++javascript+++__pycache__+++"
        "src+++python_goto+++__pycache__+++")

    l_path="/"
    w_path="\\"
    present="no"

    case "$(getOsInfo)" in
    linux*)
        for garbage in "${garbages[@]}"; do
            if [ -d "${garbage//+++/$l_path}" ]; then
                present="yes"
            fi
        done
        ;;
    msys*)
        for garbage in "${garbages[@]}"; do
            if [ -d "${garbage//+++/$w_path}" ]; then
                present="yes"
            fi
        done
        ;;
    darwin*)
        for garbage in "${garbages[@]}"; do
            if [ -d "${garbage//+++/$l_path}" ]; then
                present="yes"
            fi
        done
        ;;
    *) echo "System info not found check garbage manually!" ;;
    esac

    echo "$present"
}

function deleteCache() {
    # Function deleteCache() deletes the cache produced by the program after each run of selenium webdriver. This function first
    # gets the system info then deletes the folder '__pycache__' accordingly.
    declare -a garbages=("__pycache__+++"
        "src+++__pycache__+++"
        "src+++db+++__pycache__+++"
        "src+++dom+++__pycache__+++"
        "src+++creds+++__pycache__+++"
        "src+++errors+++__pycache__+++"
        "src+++helpers+++__pycache__+++"
        "src+++console+++__pycache__+++"
        "src+++linkedin+++__pycache__+++"
        "src+++invitation+++__pycache__+++"
        "src+++javascript+++__pycache__+++"
        "src+++python_goto+++__pycache__+++")

    l_path="/"
    w_path="\\"

    case "$(getOsInfo)" in
    linux*)
        for garbage in "${garbages[@]}"; do
            if [ -d "${garbage//+++/$l_path}" ]; then
                sudo rm -rf "${garbage//+++/$l_path}"
            fi
        done
        ;;
    msys*)
        for garbage in "${garbages[@]}"; do
            if [ -d "${garbage//+++/$l_path}" ]; then
                rm -r "${garbage//+++/$l_path}"
            fi
        done
        ;;
    darwin*)
        for garbage in "${garbages[@]}"; do
            if [ -d "${garbage//+++/$l_path}" ]; then
                sudo rm -rf "${garbage//+++/$l_path}"
            fi
        done
        ;;
    *) echo "System Information not found delete __pycache__ Manually" ;;
    esac
}

function main() {
    # Function main is the main function that starts the execution of the linkedin automator program it first checks if the
    # requirements are present or not then it takes actions accordingly.
    if python3 --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        runProgram python3.7 "linux"
    elif python2 --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        runProgram python2 "linux"
    elif python --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        runProgram python "linux"
    elif py --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        runProgram py "windows"
    else
        echo "Python is not installed"
        installPython
    fi
}

# Starting the LinkedIn automation program if no command line arguments are passed otherwise handles the command line arguments.
if [ $# -eq 0 ]; then
    # Start if no arguments are passed in the command line and also delete the pycache if present.
    main
    if [ "$(checkIfGarbage)" = "yes" ]; then
        deleteCache
    fi
else
    # Getting the command line argument passed by the user
    while getopts ":d:" opt; do
        case $opt in
        d)
            if [ "$OPTARG" = "pycache" ]; then
                if [ "$(checkIfGarbage)" = "yes" ]; then
                    deleteCache
                else
                    echo "'__pycache__' does not exist!"
                fi
            fi
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        esac
    done
fi
