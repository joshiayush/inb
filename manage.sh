#!/bin/bash

# Copyright 2023 The inb Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if [ $# -eq 0 ]; then
    exit 1
fi

project_root_dir=$(pwd)

#
# function _dcache deletes __pycache__ folders floating around python modules
#
function _dcache() {
    find "$project_root_dir/inb" -name "__pycache__" >pycache

    while IFS= read -r cache_file; do
        rm -r $cache_file
    done <pycache

    rm pycache
}

#
# function _get_code_lines count the number of code lines written so far in project
# inb
#
function _get_code_lines() {
    echo $(find inb/ -name '*.py' -exec cat {} \; | wc -l)
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
        "-v" | "--verbose")
            arg="$arg verbose"
            ;;
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
    fi
}

# call main function with the arguments given
main $@
