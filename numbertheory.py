"""
Utility functions useful for euclid problems and the like.
"""


def modadd(x, y, n):
    """
    Calculate modular addition: (x+y) mod n.

    Args: integers x and y, and a positive integer n

    >>> modadd(3, -10, 5)
    3
    >>> modadd(278, 199, 17)
    1
    """
    return (x + y) % n


def modexp(x, y, n):
    """
    Calculate modular exponentiation: x^y mod n.

    The time complexity of this algorithm is O(b^3), where
    b is the number of bits of the largest of x, y, and n.
    The algorithm performs at most n recursive calls, and
    at each call, multiplies n-bit numbers modulo n.

    The algorithm is based on the following rule:

    x^y    =      (x^floor(y/2)) ^ 2 if y is even
           =  x * (x^floor(y/2)) ^ 2 if y is odd

    Args:
      * x: an integer
      * y: a non-negative integer
      * n: a positive integer

    >>> modexp(2, 5, 6)
    2
    >>> modexp(43417, 53535, 34310)
    12053L
    >>> modexp(345343417, 542323535, 324244310)
    23504373L
    """
    if y == 0:
        return 1
    z = modexp(x, y / 2, n)
    if y % 2 == 0:
        return (z * z) % n
    else:
        return (x * z * z) % n


def euclid(a, b):
    """
    Calculates the greatest common divisor of a and b.

    Args:
      * a: a non-negative integer >= b
      * b: a non-negative integer <= a

    >>> euclid(2, 2)
    2
    >>> euclid(99, 15)
    3
    >>> euclid(95, 100)
    5
    >>> euclid(56, 14)
    14
    >>> euclid(135749, 27482)
    151
    """
    if b == 0:
        return a
    return euclid(b, a % b)


def extended_euclid(a, b):
    """
    Calculates integers x, y, d such that d = gcd(a, b) and
    ax + by = d.

    Args: non-negative integers a and b with a >= b >= 0.

    >>> extended_euclid(7, 2)
    (1, -3, 1)
    >>> extended_euclid(81, 57)
    (-7, 10, 3)
    """
    if b == 0:
        return (1, 0, a)
    (x, y, d) = extended_euclid(b, a % b)
    return (y, x - ((a / b) * y), d)


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()
