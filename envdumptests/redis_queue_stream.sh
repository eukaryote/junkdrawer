#!/bin/sh

# Encode the environment as a base64 string and push it onto a redis queue
# using redis-cli, and pull it off in another process then decode and
# extract and display the integer COUNTER in the receiver.

# This handles about 200 messages a second.

send() {
    export COUNTER=0
    while true; do
        /usr/bin/env | base64 -w 0 | redis-cli -x LPUSH myqueue > /dev/null
        echo $COUNTER
        COUNTER=$(($COUNTER + 1))
    done
}

receive() {
    while true; do
        redis-cli BRPOP myqueue 0 | tail -n 1 | base64 -d | grep COUNTER
    done
}


command="$1"
if [ "$command" != "send" -a "$command" != "receive" ]; then
    echo "usage: redis_queue_stream.sh (send|receive)"
    exit 1
fi

if [ "$command" = "send" ]; then
    send
else
    receive
fi
