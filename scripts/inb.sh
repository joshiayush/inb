#!/bin/bash

if [ $# -eq 0 ]; then
    exit 1
fi

__name__="inb"
__version__="1.51.35"

ProjectRootDirectory=$(pwd)

. "$ProjectRootDirectory/scripts/rwx.sh"
. "$ProjectRootDirectory/scripts/dcache.sh"
. "$ProjectRootDirectory/scripts/ipackages.sh"

_verbose=1
_installPackages=1
_deleteCache=1
_owners=
_modes="rwx"

while getopts "ivdo:m:hl" option; do
    case $option in
    i) _installPackages=0 ;;
    v) _verbose=0 ;;
    d) _deleteCache=0 ;;
    o) _owners=$OPTARG ;;
    m) _modes=$OPTARG ;;
    l) find inb/ -name '*.py' -exec cat {} \; | wc -l 
        exit 0 ;;
    ?) 
        # We would like to throw error showing 
        # the correct usage
    ;;
    esac
done

if [ $_installPackages -eq 0 ]; then
    installPackages $_verbose
    exit 0
fi

if [ $_deleteCache -eq 0 ]; then
    dcache
    exit 0
fi

if [ $_owners ]; then
    rwx $_owners "+" $_modes
    exit 0
fi