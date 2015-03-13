#!/usr/bin/env python

"""
Prints scrambled version of text read from stdin to stdout, keeping
the first and last letters of a word the same.
"""

import re
import sys


PAT = re.compile(r'\b([a-zA-Z]*)\b')

if __name__ == '__main__':
    for line in sys.stdin:
        for word in PAT.split(line):
            l = len(word)
            if l > 3:
                sys.stdout.write(word[0])
                sys.stdout.write(''.join(sorted(list(word[1:l - 1]),
                                                reverse=True)))
                sys.stdout.write(word[-1])
            else:
                sys.stdout.write(word)
