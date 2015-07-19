#!/bin/sh

fifo="myfifo"

i=0
while true; do
    echo $i > $fifo
    i=$(($i + 1))
done
