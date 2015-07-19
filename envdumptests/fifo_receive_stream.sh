#!/bin/sh

pipe=myfifo

test -p $pipe || mkfifo $pipe

while true
do
    if read line <$pipe ; then
        if [ "$line" = "" ] ; then
            break
        fi
        echo "$line"
    fi
done
