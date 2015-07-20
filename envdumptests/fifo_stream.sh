#!/bin/sh

# Tests base64-encoding the environment and sending it through a named pipe,
# which handles about 400 messages a second.

receive() {
    local pipe="$1"
    local line
    while true; do
        cat $pipe | base64 -d | grep COUNTER
    done
}


send() {
    local pipe="$1"
    export COUNTER=0
    while true; do
        /usr/bin/env | base64 -w 0 > $pipe
        COUNTER=$(($COUNTER + 1))
        echo $COUNTER
    done
}

pipe=myfifo
test -p $pipe || mkfifo $pipe

if [ "$1" = "send" ]; then
    send $pipe
else
    receive $pipe
fi
