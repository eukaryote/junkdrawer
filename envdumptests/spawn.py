#!/usr/bin/env python

"""
Asynchronously spawn ARGV[2] number of processes identified by path
given as ARGV[1], and exit only after they all finish.

Example: ./spawn.py ./a.out 1000
"""

import sys
from subprocess import Popen


if __name__ == '__main__':
    exe = sys.argv[1]
    count = int(sys.argv[2])
    for proc in [Popen(exe) for i in range(count)]:
        proc.wait()
