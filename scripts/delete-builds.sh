#!/bin/bash

function deleteBuilds() {
    echo "Deleting builds ..."
    echo "Deleting build dir ..."
    sudo rm -rf build
    echo "Deleting dist dir ..."
    sudo rm -rf dist
    echo "Deleting main.spec file ..."
    sudo rm main.spec
}   

deleteBuilds