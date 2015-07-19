#!/bin/sh

fifo=myfifo

test -p ${fifo} || mkfifo ${fifo}

export COUNTER="$1"
/usr/bin/env > $fifo
