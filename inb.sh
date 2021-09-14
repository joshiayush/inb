#!/bin/bash

if [ $# -eq 0 ]; then
    exit 1
fi

project_root_dir=$(pwd)

# 
# function _dcache deletes __pycache__ folders floating around python modules
# 
function _dcache() {
  find "$project_root_dir/inb" -name "__pycache__" > pycache

  while IFS= read -r cache_file; do
    rm -r $cache_file
  done < pycache

  rm pycache
}

# 
# function _allow_premissions changes the filemodes of the files in the project root 
# directory while setting the git core.filemode option to false 
# 
function _allow_permission() {
  # 
  # change file mode of the files/directories and sub-directories
  #   
  chmod 777 -R .

  # 
  # set git config core.filemode to false to tell git not to track the access bits 
  # of the files/directories
  #   
  git config core.filemode false
}

# 
# function _get_code_lines count the number of code lines written so far in project
# inb
# 
function _get_code_lines() {
    echo $(find inb/ -name '*.py' -exec cat {} \; | wc -l )
}

# 
# function _install installs the requirements for project inb
# 
function _install() {
    local verbose=$1
    if [ -z $verbose ]; then
        verbose=1
    fi
    if [ -f "$project_root_dir/requirements.txt" -o -s "$project_root_dir/requirements.txt" ]; then
        if [ $verbose -eq 0 ]; then
            python3 -m pip install -r requirements.txt
        else
            python3 -m pip install -r requirements.txt >/dev/null
        fi
    fi
}

# 
# function _parse_args parses the arguments given to the program
# 
_parse_args() {
    arg=
    mutually_exclusive_group_found=false
    while [ "${1:-}" != "" ]; do
        case "$1" in
        "-i" | "--install")
            if [ $mutually_exclusive_group_found = false ]; then
                arg="install"
                mutually_exclusive_group_found=true
            fi
            ;;
        "-d" | "--dcache")
            if [ $mutually_exclusive_group_found = false ]; then
                arg="dcache"
                mutually_exclusive_group_found=true
            fi
            ;;
        "-l" | "--line")
            if [ $mutually_exclusive_group_found = false ]; then
                arg="line"
                mutually_exclusive_group_found=true
            fi
            ;;
        "-p" | "--rwx")
            if [ $mutually_exclusive_group_found = false ]; then
                arg="rwx"
                mutually_exclusive_group_found=true
            fi
            ;;
        "-v" | "--verbose")
            arg="$arg verbose"
        esac
        shift
    done
    echo $arg
}

# 
# entry point
# 
function main() {
    arg=$(_parse_args $@)
    if [[ $arg == install* ]]; then
        if [[ $arg =~ "verbose" ]]; then
            _install 0
        else
            _install
        fi
    elif [[ $arg == "dcache" ]]; then
        _dcache
    elif [[ $arg == "line" ]]; then
        _get_code_lines
    elif [[ $arg == "rwx" ]]; then
        _allow_permission
    fi
}

# call main function with the arguments given
main $@