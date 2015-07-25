#!/bin/bash -eu

run () {
    i=0 
    while [[ "$i" -lt "$2" ]]
    do
        $1 >/dev/null 2>&1
        i=$(($i + 1)) 
    done
}

run "$@"
