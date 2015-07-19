import os
import errno
import base64

import ujson

COUNTER_KEY = 'COUNTER'

FIFO_PATH = 'myfifo'
SOCKET_PATH = 'mysocket'
REDIS_QUEUE = 'myqueue'
REDIS_CHANNEL = 'mychannel'


def to_json(counter):
    d = dict(os.environ)
    d[COUNTER_KEY] = counter
    return ujson.dumps(d)


def to_json_base64(counter):
    return base64.b64encode(to_json(counter))


def from_json(jsonstr):
    if not jsonstr:
        return
    data = ujson.loads(jsonstr)
    if isinstance(data, int):
        return data
    return data[COUNTER_KEY]


def from_json_base64(b64str):
    if b64str:
        return from_json(base64.b64decode(b64str))


def mkfifo(path=FIFO_PATH):
    try:
        os.mkfifo(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
