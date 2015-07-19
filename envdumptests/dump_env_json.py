#!/usr/bin/env python

from __future__ import print_function

import os

import ujson

print(ujson.dumps(dict(os.environ)))
