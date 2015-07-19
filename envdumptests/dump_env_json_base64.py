#!/usr/bin/env python

"""
This takes about 50 milliseconds on my laptop (cpython 2.7.9).

The times below are for the line in question with the appropriate imports
commented out, because the extra time for the json ones is mostly a result of
importing ujson, not the actual `dumps` call.
"""

from __future__ import print_function

import os
import base64

import ujson

# print(os.environ)  # ~0.043
# print(dict(os.environ))  # ~0.043
# print(ujson.dumps(dict(os.environ)))  # ~0.052
print(base64.b64encode(ujson.dumps(dict(os.environ))))  # ~0.052
