#!/bin/sh

pipe=myfifo

test -p $pipe || mkfifo $pipe

cat $pipe
