#!/bin/bash

function build() {
    echo "Building linkedin-bot ..."
    /usr/bin/python3.7 -m PyInstaller ./linkedin-bot/main.py
    echo "Executing binary file main ..."
    ./dist/main/main
}   

build