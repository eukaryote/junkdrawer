#!/usr/bin/env python

import sys
import collatz as c
import utils


def usage():
    print("""%s [-s] low_int_val high_int_val\n
Examples:\n
  Generate image from 1 to 100; don't show it\n
  %s 1 100\n
  Generate image from 100 to 300, and show it\n
  %s -s 100 300
""" % ((sys.argv[0],) * 3))
    sys.exit()

web_dpi = 72
args = sys.argv
num_args = len(args)
interactive = utils.is_interactive(args)

if __name__ == '__main__':
    # do basic arg checking before the expensive pylab import
    if not interactive:
        if num_args < 3 or num_args > 4:
            usage()
        elif num_args == 4 and args[1] != '-s':
            usage()
        elif num_args == 3 and False in map(utils.is_num_arg, args[1:]):
            usage()

# from pylab import *
from pylab import (
    yticks, arange, bar, title, xlabel, xlim, xticks,
    ylabel, ylim, savefig, show)
import pylab


def prepare(low, high):
    """ Prepare a barchart plotting y=collatz_len(x) against x, but
    down't save it or display it yet. """
    assert high > low

    low_high_range = high - low + 1

    # width is a value from 0 to 1 representing how much of the width
    # allocated to each column will be colored in (e.g., .1 means 10%
    # is colored in, and 90% is space between the columns).
    width = 1
    # linewidth is the width of the line around each column
    linewidth = 1
    if low_high_range >= 500:
        linewidth = 0

    xvals = range(low, high + 1)
    yvals = tuple(map(c.collatz_len, xvals))
    max_yval = max(yvals)

    ind = arange(low, high + 1)  # the x locations for the groups
    bar(ind, yvals, width, color='b', linewidth=linewidth)

    title(r'Length of Collatz sequence: $%d \le n \le %d$' % (low, high))

    xlabel('n')
    xlim(low, high + 1)

    xtick_len = low_high_range / 10
    # low xtick val is the next value higher than low divisible by 10
    low_xtick_val = low + xtick_len
    low_xtick_val = low_xtick_val - (low_xtick_val % 20)
    xtick_vals = arange(low_xtick_val, high + 2, xtick_len)
    # the xtick value should be in the middle of column
    xticks(xtick_vals + 0.5, xtick_vals)

    ylabel('Sequence Length')
    top_ytick = max_yval + (10 - (max_yval % 10)) + 1
    ylim(0, top_ytick)

    yticks(arange(10, top_ytick, 10))


def filename_and_ext(str):
    pieces = str.split('.')
    num_pieces = len(pieces)
    if num_pieces == 1 or (num_pieces == 2 and pieces[0] == ''):
        return (str, None)
    return '.'.join(pieces[0:-1]), pieces[-1]


def save(low, high, filename='length_%d_to_%d.png'):
    """ Save the prepared image for the given low and high values to
    a file, using the filename string pattern for the name; the filename
    must have two variable markers for the low and high values to be
    interpolated into. """
    base_filename_and_ext = filename % (low, high)
    base_filename, ext = filename_and_ext(base_filename_and_ext)

    figure = pylab.gcf()
    default_size = figure.get_size_inches()
    default_dpi = figure.get_dpi()

    figure.set_dpi(web_dpi)

    custom_size = tuple(map(lambda n: n * 2.0, default_size))
    savefig(base_filename + "_small." + ext)
    figure.set_size_inches(custom_size)

    figure.set_dpi(web_dpi * 2)
    savefig(base_filename + "_large." + ext)

    figure.set_size_inches(default_size)
    figure.set_dpi(default_dpi)


if __name__ == '__main__':
    # This only runs if we didn't exit at the top; we would have exited if
    # it was a non-interactive session and there were not 3 or 4 args
    # (including the program name as arg[0]).
    if not interactive:
        if args[1] == "-s":
            display = True
            low, high = args[2], args[3]
        else:
            display = False
            low, high = args[1], args[2]
        low, high = int(low), int(high)
        prepare(low, high)
        save(low, high)
        if display:
            show()
