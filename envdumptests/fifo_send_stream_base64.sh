#!/bin/sh

fifo="myfifo"

i=0
while true; do
    export COUNTER=$i
    bash -c 'env | base64' > $fifo
    i=$(($i + 1))
    echo $i
done
