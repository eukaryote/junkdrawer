#!/usr/bin/env python

"""
Generate a graphviz dot file.

Usage:

./graph.py n max_depth
"""

import sys
import utils


def usage():
    print("""%s n max_depth\n
%s -c n max_depth max_nodes

Generate a Graphviz dot file for the Collatz tree rooted at n.

If the first command is given, the tree includes even numbers
and stops after max_depth levels have been output.

If the second command is given, then it outputs a compressed
tree that omits all even numbers, and it stops either
max_depth levels have been exhausted or max_nodes nodes have
been output (whichever occurs first).

Examples:\n

Generate file for tree (even and odd nodes) rooted at 1 to
a maximum depth of 10.

  %s 1 10\n

Generate file for compressed tree (odd nodes only) rooted at 1
to a maximum depth of 5, following branches of only even nodes
no more than 10 deep.

  %s -c 1 5 10
""" % ((sys.argv[0],) * 4))
    sys.exit()

args = sys.argv
num_args = len(args)
interactive = utils.is_interactive(args)

if __name__ == '__main__':
    # do basic arg checking before the expensive pylab import in collatz
    if not interactive:
        if num_args == 3:
            if False in (map(utils.is_num_arg, args[1:])):
                usage()
        elif num_args == 5:
            if args[1] != '-c' or False in map(utils.is_num_arg, args[2:]):
                usage()
        else:
            usage()

import collatz as c


def begin(dotfile):
    dotfile.write('''digraph unix {
  node [color=lightblue2, style=filled];\n''')


def end(dotfile):
    dotfile.write('}\n')


def middle(dotfh, initial=1, max_depth=10):
    nodes = c.collatz_tree(initial=initial, max_depth=max_depth, all_info=True)
    # skip the root node, which appears again as the parent of the next node
    nodes.next()
    for (n, prev_n, depth) in nodes:
        prev_n_mod3, n_mod3 = prev_n % 3, n % 3
        if n & 1:
            dotfh.write('\n "%d (%d)" [style=filled,color=".7 .3 1.0"];\n'
                        % (n, n_mod3))
            edge_conf = "[style=bold]"
        else:
            dotfh.write('\n  "%d (%d)" [style=filled,color=lightblue2];\n'
                        % (n, n_mod3))
            edge_conf = "[style=dotted]"
        dotfh.write('  "%d (%d)" -> "%d (%d)" %s;\n'
                    % (prev_n, prev_n_mod3, n, n_mod3, edge_conf))


def middle_c(dotfh, initial=1, max_depth=8, max_nodes=128):
    nodes = c.collatz_tree_compressed(initial=initial, max_depth=max_depth,
                                      all_info=True)
    nodes = utils.take_n(nodes, max_nodes)
    nodes.next()
    dotfh.write('\n node [style=filled, color=".7 .3 1.0"];\n')
    for (n, prev_odd_n, num_evens, depth) in nodes:
        prev_odd_n_mod3, n_mod3 = prev_odd_n % 3, n % 3
        if num_evens:
            edge_conf = '[label="%d"]' % num_evens
        else:
            edge_conf = ''
        dotfh.write('  "%d (%d)" -> "%d (%d)" %s;\n'
                    % (prev_odd_n, prev_odd_n_mod3, n, n_mod3, edge_conf))


if __name__ == '__main__':
    # This only runs if we didn't exit at the top; we would have exited if
    # it was a non-interactive session and there were not 3 args
    # (including the program name as arg[0]).
    if not interactive:
        if num_args == 3:
            initial, max_depth = int(args[1]), int(args[2])
            compressed = False
        else:
            assert args[1] == '-c'
            initial, max_depth, max_nodes = (int(args[2]), int(args[3]),
                                             int(args[4]))
            compressed = True
        if compressed:
            filename_base = ('compressed_tree_on_%d_max_depth_%d_max_nodes_%d'
                             % (initial, max_depth, max_nodes))
        else:
            filename_base = 'tree_on_%d_max_depth_%d' % (initial, max_depth)

        dotfilename = filename_base + '.dot'
        print('Generating dot file: %s' % dotfilename)
        dotfh = open(dotfilename, 'w')
        try:
            begin(dotfh)
            if compressed:
                middle_c(dotfh, initial=initial, max_depth=max_depth,
                         max_nodes=max_nodes)
            else:
                middle(dotfh, initial=initial, max_depth=max_depth)
            end(dotfh)
        finally:
            dotfh.close()
        cmd = 'dot -Tpng %s -o %s.png' % (dotfilename, filename_base)
        print('Running: %s' % cmd)
        retcode = utils.generate_graph_image(dotfilename, '%s.png'
                                             % filename_base)
        if retcode == 0:
            print('Generated tree image: %s.png' % filename_base)
        else:
            print('Subprocess returned error code: %d' % retcode)
        sys.exit(retcode)
