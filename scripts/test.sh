#!/bin/bash

source /Python/linkedin-bot/scripts/garbage.sh

function _test() {
    python3.7 linkedin-bot/test.py
}

_test
if [ "$(checkIfGarbage)" = "yes" ]; then
    deleteCache
fi