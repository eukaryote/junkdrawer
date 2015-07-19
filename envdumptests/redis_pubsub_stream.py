#!/usr/bin/env python

"""
Tests using redis pub/sub to send/receive a stream of messages.

Handles about 10,000 simple counter messages a second, and redis was able to
buffer 200K counter messages without blocking the sender, and the receiver
did receive all messages even when slowing it down by introducing a sleep.

If there are no subscribers when events are published, then the events
are lost, which makes raw pub/sub less attractive than using a redis
list as a queue
"""

from __future__ import print_function

import sys
import redis
import time

from util import REDIS_CHANNEL, from_json, to_json


def receive(r, channel, sleep=None):
    p = r.pubsub()
    p.subscribe(channel)
    while True:
        message = p.get_message(ignore_subscribe_messages=True)
        if message:
            print(from_json(message['data']))
            # extra sleep if requested
            if sleep is not None:
                time.sleep(sleep)
        else:
            time.sleep(0.001)  # always sleep when nothing received


def send(r, channel):
    i = 0
    while True:
        r.publish(channel, to_json(i))
        print(i)
        i += 1


if __name__ == '__main__':
    r = redis.StrictRedis()
    command = sys.argv[1]
    assert command in ('send', 'receive')
    if command == 'receive':
        sleep = float(sys.argv[2]) if sys.argv[2:] else None
        receive(r, REDIS_CHANNEL, sleep=sleep)
    else:
        send(r, REDIS_CHANNEL)
