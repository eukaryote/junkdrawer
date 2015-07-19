#!/usr/bin/env python

"""
Tests using a redis list as a simple queue, sending as quickly as possible
from one process and receiving as quickly as possible in another.

Handles about 8,000 messages a second (simple integer counter), 5,000 messages
a second (ujson-encoded os.environ plus counter), and doesn't block the sender
until lots more messages have been sent than we will send (may need redis.conf
tweaks), so this looks better than all the other simple options tried.

Can be extended to a reliable queue that handles consumer failures
by using RPOPLPUSH to push the popped message onto a processing queue,
and another client may monitor the processing list for items that have
been there too long and put them back on the primary queue.
"""

import sys
import time

import redis

from util import REDIS_QUEUE, to_json, from_json


def receive(r, queue, sleep=None):
    while True:
        channel, data = r.brpop(queue)
        print(from_json(data))
        if sleep is not None:
            time.sleep(sleep)


def send(r, queue):
    counter = 0
    while True:
        r.lpush(queue, to_json(counter))
        counter += 1


if __name__ == '__main__':
    r = redis.StrictRedis()
    command = sys.argv[1]
    assert command in ('send', 'receive')
    sleep = float(sys.argv[2]) if sys.argv[2:] else None
    if command == 'send':
        send(r, REDIS_QUEUE)
    else:
        receive(r, REDIS_QUEUE, sleep=sleep)
