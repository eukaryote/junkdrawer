#!/bin/sh

# takes about 1 ms

pipe="myfifo"

test -p $pipe || mkfifo $pipe
/usr/bin/env > $pipe
