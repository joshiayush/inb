#!/bin/bash 

function runProgram() { $1 src/main.py; }

if python3 --version | grep "Python*" > /dev/null; then
    echo "Python is installed"
    runProgram python3
elif python2 --version | grep "Python*" > /dev/null; then
    echo "Python is installed"
    runProgram python2
elif python --version | grep "Python*" > /dev/null; then
    echo "Python is installed"
    runProgram python
else
    echo "Python is not installed"
fi