from __future__ import print_function

"""
Takes a stream of prime numbers, one per line, as input and determines the
proportion of primes that have a given digit as the least significant digit
(in base 10).

For example, the following shows primes from 10 to 1,000,000:

primes 10 1000000 | ./primedigit.py
Last Digit |  Count  |  Ratio
--------------------------------
% 1           19617     1.001225
% 3           19664     1.003624
% 7           19620     1.001378
% 9           19593     1.000000
"""

import sys

if __name__ == '__main__':
    primes_by_last_digit = {}

    for str in sys.stdin.xreadlines():
        num = int(str)
        last_digit = num % 10
        new_count = primes_by_last_digit.get(last_digit, 0) + 1
        primes_by_last_digit[last_digit] = new_count

    min_count = min(primes_by_last_digit.itervalues())

    last_digits = sorted(list(primes_by_last_digit.keys()))

    print("Last Digit |  Count  |  Ratio")
    print("--------------------------------")
    for last_digit in last_digits:
        d = primes_by_last_digit[last_digit]
        print("%% %d           %d \t%f" %
              (last_digit, d, d / float(min_count)))
