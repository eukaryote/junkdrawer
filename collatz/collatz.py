from heapq import heappop, heappush
from itertools import count, imap
import utils
import math

try:
    range = xrange
except NameError:
    pass


def collatz_tree(initial=1, all_info=True, max_depth=None):
    ''' Generate the tree of Collatz predecessors starting with 1
    proceeding layer by layer through the tree, with elements
    at a given layer returned in ascending order.

    This tree, also known as the predecessor tree, is the sequence
    of numbers reachable by doing the inverse operations
    (for each n, always perform the 2n rule and perform the
    (n-1)/3 when it is defined (when it results in an odd integer).

    If all_info is False, then the generator is over just the number
    n itself. If all_info is True (default), then each element of the
    generator is (n, prev_n, depth), where prev_n is the previous number
    (for all n other than 1) that yielded n (or the parent node
    in the tree) and depth is the depth of the n, with the depth
    of the initial value being 0.

    If max_depth is given, it must be a non-negative integer, and the
    generator will stop after the processing that layer of the tree
    (where the initial level is 0).

    If the Collatz conjecture is true, then this generator would
    eventually include every positive integer, with no repeated integers
    and no cycles (except the trivial 1, 2, 4, 1).'''
    assert max_depth is None or max_depth >= 0
    heap = [(0, initial, None, double_gen(initial))]
    while True:
        (depth, n, prev_n, higher_gen) = heappop(heap)
        if max_depth is not None and depth > max_depth:
            raise StopIteration()
        if all_info:
            yield (n, prev_n, depth)
        else:
            yield n
        depth += 1
        if n != 4 and not (n & 1):
            n_lower = upinv(n)
            # if there was an inverse and it's not a power of two
            if n_lower and not (n_lower and not (n_lower & (n_lower - 1))):
                heappush(heap, (depth, n_lower, n, double_gen(n_lower)))
        # this must be pushed after the lower, if any, because
        # the heap ordering only considers the first tuple element
        # and we wish lower elements at a given level to come first
        n_higher = higher_gen.next()
        heappush(heap, (depth, n_higher, n, higher_gen))


def collatz_tree_compressed(initial=1, all_info=True, max_depth=None,
                            max_evens=None):
    assert ((max_depth is None or max_depth >= 0) and
            (max_evens is None or max_evens > 0))
    prev_odd_n, depth, num_evens = None, 0, 0
    heap = [(initial, prev_odd_n, depth, num_evens, double_gen(initial))]
    while True:
        # if heap is empty, then we're finished to depth of max_depth and have
        # checked as many evens as requr
        if not heap:
            raise StopIteration()
        # pop current lowest n
        (n, prev_odd_n, depth, num_evens, higher_gen) = heappop(heap)
        n_higher = higher_gen.next()
        # if n is even, then we don't yield it in the compressed tree,
        # but we must keep track of how many we skip so that we can
        # include that information when we finally get to an odd number.
        if not (n & 1):  # if even:
            n_lower = upinv(n)
            # if there is a lower and it's not 1 or a power of two:
            if (n_lower and n != 1
                    and not (n_lower and not (n_lower & (n_lower - 1)))):
                # then we push it back and increment the num_evens and
                # depth, unless finished
                if ((max_evens is None or num_evens < max_evens)
                        and depth < max_depth):
                    heappush(heap, (n_lower, prev_odd_n, depth + 1,
                             num_evens + 1, utils.double_gen(n_lower)))
            # if we're not at the end of a string of max_evens even numbers
            # in a row, push on the next higher even, while keeping
            # prev_odd_n and incrementing num_evens
            if max_evens is None or num_evens <= max_evens:
                heappush(heap, (n_higher, prev_odd_n, depth, num_evens + 1,
                         double_gen(n_higher)))
        else:  # if odd:
            if all_info:
                yield (n, prev_odd_n, num_evens, depth)
            else:
                yield n
            # push the next even value, keeping same depth, updating prev_odd,
            # and resetting num_evens back to 0, as long as we're not finished
            heappush(heap, (n_higher, n, depth, 0, double_gen(n_higher)))


def double_gen(x):
    while True:
        x += x
        yield x


def collatz_seq(x):
    ''' Generate the Collatz sequence for the non-positive integer x. '''
    assert x > 0, "Undefined for non-positive x"
    while x != 1:
        if not (x & 1):
            x = x >> 1
        else:
            x = (x + x + x + 1)
        yield x


def collatz_len(x):
    ''' Determine the length of the Collatz sequence of the non-positive x,
        or the number of integers until the result is 1. '''
    assert x > 0, "Undefined for non-positive x"
    c = 0
    while x != 1:
        if not (x & 1):  # x/2, then incr 1
            x = x >> 1
            c += 1
        else:           # 3x+1, x/2, then incr 2 (minor optimization)
            x = (x + x + x + 1) >> 1
            c += 2
    return c


def collatz_lens(low=1, high=None):
    ''' Generate the length of the Collatz sequence for each
    consecutive integer from low (default = 1) to high (optional).
    If high is given, then the generator ends after returning the
    length for that element. For example, the generator for low=1
    and high = 3 would yield (collatz_len(1), collatz_len(2),
    collatz_len(3).'''
    assert low > 0 and (high is None or high > low)
    all_gen = imap(collatz_len, count(low))
    if high is None:
        return all_gen
    else:
        return utils.take_n(all_gen, high - low + 1)


# helper functions for interactive experimentation

# up generates the next Collatz value for an x assumed to be odd
def up(x):
    ''' Return the 3x+1 value for x. '''
    return x + x + x + 1


# down generates the next Collatz value for an x assumed to be even
def down(x):
    ''' Return the x/2 value for x. '''
    return x >> 1


# upinv is the inverse of up
def upinv(x):
    ' Return the y such that x=3y+1, if any (i.e., (x-1)/3 or None). '
    (m, n) = divmod(x - 1, 3)
    if not n:
        return m


# downinv is the inverse of down
def downinv(x):
    ' Return the y such that x=y/2 (i.e., 2x). '
    return x << 1


def len_interval_gen(low, high):
    ' Create a generator over the collatz lengths of x for low <= x <= high.'
    return imap(collatz_len, range(low, high + 1))


def mean_len_interval(low, high):
    ''' Find the average collatz interval from low to high, inclusive. '''
    total = 0
    count = 0
    for i in len_interval_gen(low, high):
        total += i
        count += 1
    return total / float(count)


def stddev_len_interval(low, high):
    ''' Find the standard deviation of the collatz length for n in
    the interval from low to high, inclusive. '''
    return stddev(len_interval_gen(low, high))


def stddev(iter):
    ''' Calculate the standard deviation of the elements in the given
    iterable (this is a one-pass algorithm).
    http://mail.python.org/pipermail/python-dev/2004-January/041997.html
    '''
    n = 0
    x = 0.
    xx = 0.
    for y in iter:
        n += 1
        x += y
        xx += y * y
    x /= n
    xx /= n
    var = max(0, xx - x * x)
    dev = math.sqrt(var)
    return dev
