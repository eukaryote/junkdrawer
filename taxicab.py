#!/usr/bin/env python

"""
Calculate 'taxicab' numbers that are positive integers that are the sum of
two perfect powers in multiple ways.
"""

from __future__ import print_function

import sys
import argparse

try:
    range = xrange
except NameError:
    pass

DEFAULT_POWER = 3
DEFAULT_WAYS = 2


def calculate(upper, power=DEFAULT_POWER, ways=DEFAULT_WAYS):
    results = {}
    for i in range(1, upper):
        for j in range(i + 1, upper):
            n = i ** power + j ** power
            results.setdefault(n, []).append((i, j))
    for k in list(results):
        if len(results[k]) < ways:
            del results[k]
    return results


def parse_args(argv=None):
    desc = ("Calculate 'taxicab' numbers, which are positive integers that "
            "are representable as the sum of two perfect powers in multiple "
            "ways.")
    epilog = ("The well-known taxicab number is 1729, which was the number "
              "of a taxicab that Hardy took to visit Ramanujan in hospital "
              "and Ramanujan noted is the smallest number that is the sum "
              "of two cubes in two different ways, since 12^3 + 1^3 == 1729 "
              "and 10^3 + 9^3 == 1729. "
              "This program calculates numbers like this, allowing the power "
              "(3 above) and the minimum number of ways (two different "
              "ways above) to be configurable, but defaulting to the "
              "Ramanujan values.")
    parser = argparse.ArgumentParser(description=desc, epilog=epilog)

    _help = ("restrict to integers that are representable as sum of powers "
             "in at least the given number of different WAYS [default=%s]"
             % DEFAULT_WAYS)
    parser.add_argument('-w', '--ways', type=int, help=_help,
                        metavar='WAYS', default=DEFAULT_WAYS)

    _help = ("restrict to integers that are the sum of two different integers "
             "to the given POWER in multiple ways [default=%s]"
             % DEFAULT_POWER)
    parser.add_argument('-p', '--power', type=int, help=_help,
                        metavar='POWER', default=DEFAULT_POWER)

    _help = ("upper bound for the two integers to be used for finding pairs "
             "of powers that satisfy the constraints -- must be a positive "
             "integer")
    parser.add_argument('upper', type=int, help=_help, metavar='UPPER')

    args = parser.parse_args(argv or sys.argv[1:])

    for name in ['ways', 'power', 'upper']:
        if getattr(args, name) < 1:
            parser.error("%s must be a positive integer" % (name.upper()))

    return args


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    elems = calculate(args.upper + 1, power=args.power, ways=args.ways)
    for cubes_sum, pairs in sorted(elems.items()):
        print('%s: %s' % (cubes_sum, pairs))


if __name__ == '__main__':
    main()
