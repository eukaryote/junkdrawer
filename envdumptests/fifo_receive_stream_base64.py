#!/usr/bin/env python

from __future__ import print_function

from util import FIFO_PATH
import base64

while True:
    with open(FIFO_PATH, 'r', 0) as f:
        print(base64.b64decode(f.read()))
