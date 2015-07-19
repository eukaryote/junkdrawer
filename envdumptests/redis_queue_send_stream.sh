#!/bin/sh

# Tests sending a stream of messages, each in its own python process,
# which highlights just how big of an impact python startup time
# has when trying to run lots of short-lived processes.

i=0

while true; do
    python redis_queue_send_one.py $i
    echo "$i"
    i=$(($i + 1))
done
