#!/usr/bin/env python

"""
UDS is very fast, obviously, sending and receiving about 30,000 messages a
second when the message is just an integer counter, and about 6,000 messages
a second when we json-encode the environment and send it over the socket
and unpack it on the other side.

The sender will block eventually if the receiver can't keep up.
"""

from __future__ import print_function

import sys
import os
import errno
import time
import socket

from util import SOCKET_PATH, from_json, to_json


def receive(path=SOCKET_PATH, sleep=None):
    try:
        os.unlink(path)
    except OSError:
        if os.path.exists(path):
            raise

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(path)
    sock.listen(1)

    while True:
        conn, _ = sock.accept()
        try:
            f = conn.makefile()
            while True:
                data = f.readline()
                if not data:
                    break
                print(from_json(data))
                if sleep is not None:
                    time.sleep(sleep)
        finally:
            conn.close()


def send(path=SOCKET_PATH):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Wait for receiver to start
    while True:
        try:
            sock.connect(path)
            break
        except socket.error as e:
            if e.errno != errno.ECONNREFUSED:
                raise
            time.sleep(1)
    i = 0
    try:
        f = sock.makefile()
        while True:
            print(i)
            print(to_json(i), file=f)
            i += 1
    except socket.error as e:
        if e.errno != errno.EPIPE:
            raise
    finally:
        sock.close()


if __name__ == '__main__':
    command = sys.argv[1]
    assert command in ('send', 'receive')
    if command == 'send':
        send()
    else:
        receive(sleep=float(sys.argv[2]) if sys.argv[2:] else None)
