import subprocess as p


def is_num_arg(str):
    ''' Determine whether string is a positive int string. '''
    try:
        return int(str) > 0
    except (TypeError, ValueError):
        return False


def is_interactive(args):
    """ Determine whether the args indicate an interactive session,
    using the guidelines that it is interactive if run with no
    args at all (for loading into a python session in emacs)
    or if run by ipython or if it includes the '-i' flag."""
    num_args = len(args)
    assert num_args > 0
    if num_args == 1:
        return True
    return args[0].endswith('ipython') or '-i' in args


def generate_graph_image(dot_filename='tmp.dot', out_filename='tmp.png'):
    cmd = 'dot -Tpng %s -o %s' % (dot_filename, out_filename)
    return p.call(cmd.split(r'\s'), shell=True)


def take_n(iterable, n):
    ''' Create a generator that yields n items from the given iterable. '''
    itr = iter(iterable)
    if n < 1:
        raise StopIteration()
    i = 0
    while i < n:
        yield itr.next()
        i += 1
