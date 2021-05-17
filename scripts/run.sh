#!/bin/bash

function main() {
    # Function main is the main function that starts the execution of the linkedin automator program it first checks if the
    # requirements are present or not then it takes actions accordingly.
    source /Python/linkedin-bot/scripts/execute.sh

    if python3 --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        execute python3.7 "linux"
    elif python2 --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        execute python2 "linux"
    elif python --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        execute python "linux"
    elif py --version | grep "Python*" >/dev/null; then
        echo "Python is installed"
        execute py "windows"
    else
        source /Python/linkedin-bot/scripts/python.sh
        echo "Python is not installed"
        installPython
    fi
}

source /Python/linkedin-bot/scripts/garbage.sh

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
