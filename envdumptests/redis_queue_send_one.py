#!/usr/bin/env python

"""
Send a single message (os environment as json, including the sys.argv[1]
counter) to a redis list.
"""

from __future__ import print_function

import sys

import redis

from util import REDIS_QUEUE, to_json

r = redis.StrictRedis()
r.lpush(REDIS_QUEUE, to_json(sys.argv[1]))
print(sys.argv[1])
