#!/usr/bin/env python

"""
Sender and receiver both block on the fifo while waiting for other.

Performance is about 7,000 messages a second for a simple integer counter
message (with no sleep), but messages are missed when the receiver can't keep
up.
"""

from __future__ import print_function

import sys

from util import mkfifo, FIFO_PATH, to_json, from_json


def receive(path=FIFO_PATH, sleep=None):
    mkfifo(path)
    with open(path, 'r', 0) as f:
        while True:
            data = f.readline()
            if not data:
                return
            print(from_json(data))


def send(path=FIFO_PATH):
    mkfifo(path)
    counter = 0
    with open(path, 'w') as f:
        while True:
            print(to_json(counter), file=f)
            print(counter)
            counter += 1


if __name__ == '__main__':
    command = sys.argv[1]
    assert command in ['send', 'receive']
    if command == 'send':
        send()
    else:
        receive(sleep=float(sys.argv[2]) if sys.argv[2:] else None)
