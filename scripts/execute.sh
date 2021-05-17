#!/bin/bash

function execute() {
    # Here the program start its execution `$1` is the first argument of the function `runProgram` and its value is the python
    # interpreter i.e., python[2/3], we check the system here because Windows uses '\' for navigation and Linux '/'.
    if [ "$2" = "linux" ]; then
        $1 linkedin-bot/main.py
    elif [ "$2" = "windows" ]; then
        $1 linkedin-bot\main.py
    else
        echo "System not identified"
    fi
}