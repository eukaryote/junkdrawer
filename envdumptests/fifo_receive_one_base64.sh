#!/bin/sh

pipe=myfifo

test -p $pipe || mkfifo $pipe

read line <$pipe
echo "$line" | base64 -d | grep COUNTER
