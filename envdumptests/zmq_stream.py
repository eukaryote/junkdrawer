#!/usr/bin/env python

from __future__ import print_function

import sys
import time
import zmq


def receive(context, port=5555, sleep=None):
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)

    while True:
        message = socket.recv()
        print(int(message))
        socket.send(b'')

        if sleep is not None:
            time.sleep(sleep)


def send(context, port=5555):
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:%s" % port)

    counter = 0
    while True:
        socket.send(str(counter).encode('ascii'))
        socket.recv()
        print(counter)
        counter += 1


if __name__ == '__main__':
    command = sys.argv[1]
    assert command in ('send', 'receive')
    context = zmq.Context()
    if command == 'send':
        send(context)
    else:
        receive(context, sleep=float(sys.argv[2]) if sys.argv[2:] else None)
