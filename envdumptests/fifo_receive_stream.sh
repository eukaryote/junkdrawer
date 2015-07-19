#!/bin/sh

pipe=myfifo

test -p $pipe || mkfifo $pipe

while true
do
    if read line <$pipe ; then
        [ "$line" = "" ] && break
        echo $line
        echo
    fi
done
