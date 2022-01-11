#!/bin/bash

# Copyright 2021, joshiayus Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of joshiayus Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
