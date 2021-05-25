#!/bin/bash

declare -a garbages=("__pycache__+++"
    "linkedin-bot+++__pycache__+++"
    "linkedin-bot+++DOM+++__pycache__+++"
    "linkedin-bot+++goto+++__pycache__+++"
    "linkedin-bot+++tests+++__pycache__+++"
    "linkedin-bot+++creds+++__pycache__+++"
    "linkedin-bot+++errors+++__pycache__+++"
    "linkedin-bot+++helpers+++__pycache__+++"
    "linkedin-bot+++console+++__pycache__+++"
    "linkedin-bot+++linkedin+++__pycache__+++"
    "linkedin-bot+++database+++__pycache__+++"
    "linkedin-bot+++messages+++__pycache__+++"
    "linkedin-bot+++invitation+++__pycache__+++"
    "linkedin-bot+++javascript+++__pycache__+++")

l_path="/"
w_path="\\"
present="no"

source /Python/linkedin-bot/scripts/os-type.sh

function checkIfGarbage() {
    # Function checkIfGarbage() checks if the __pycache__ garbage is present, if yes then it returns a string 'yes' otherwise does
    # not return anything.
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
