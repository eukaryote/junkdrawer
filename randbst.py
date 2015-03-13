import random
from cPickle import dump, load

from pprint import PrettyPrinter, pformat, pprint


pp = PrettyPrinter(indent=1)


class Ref(object):
    pass


class Node(dict):

    def __init__(self, key, value, indict=None):
        if indict is None:
            indict = {}
        dict.__init__(self, indict)
        self.key = key
        self.value = value
        self.size = 1

    def __getattr__(self, attr):
        return self.get(attr, None)

    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            dict.__setattr__(self, attr, value)
        else:
            if value is not None:
                self.__setitem__(attr, value)
            elif attr in self:
                self.__delitem__(attr)

    def __getstate__(self):
        return (self.key, self.value, self.size, self.left, self.right)

    def __setstate__(self, tup):
        if tup[0]:
            self.key = tup[0]
        if tup[1]:
            self.value = tup[1]
        if tup[2]:
            self.size = tup[2]
        if tup[3]:
            self.left = tup[3]
        if tup[4]:
            self.right = tup[4]

    def __getnewargs__(self):
        return self.key, self.value


class Tree(object):

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def __str__(self):
        return "Tree[]" if self.root is None else pformat(self.root)

    __repr__ = __str__

    def __getstate__(self):
        return self.root

    def __setstate__(self, n):
        self.root = n


def put(tree, key, value, debug=False):
    if debug:
        print("put[begin](%s, %s); tree.root:" % (key, value))
    if debug:
        print(tree)
    ref = Ref()
    ref.old_value, ref.is_new = None, False
    tree.root = insert_random(tree.root, key, value, ref, debug=debug)
    if debug:
        print("put[end](%s, %s); tree.root:" % (key, value))
        print(tree)
        print("\n")
    return ref.old_value if not ref.is_new else None


def get(tree, key, debug=False):
    node = node_get(tree.root, key, debug=False)
    return node.value if node else None


def node_get(node, key, debug=False):
    if node is None or key is None:
        return None
    if key < node.key:
        return node_get(node.left, key, debug)
    elif key > node.key:
        return node_get(node.right, key, debug)
    else:
        return node


def insert_random(node, key, value, ref, debug=False):
    if debug:
        print("insert_random(begin): key=%s, value=%s, old_value=%s"
              % (key, value, ref.old_value))
    if debug:
        pp.pprint(node)
    if node is None:
        node = Node(key, value)
        ref.is_new = True
        if debug:
            print("insert_random(exit node was None): key=%s, value=%s, "
                  "old_value=%s" % (key, value, ref.old_value))
        if debug:
            pp.pprint(node)
        return node
    if random.random() * node.size < 1.0:
        node = insert_at_root(node, key, value, ref, debug=debug)
        if debug:
            print("insert_random(exit insert_at_root): key=%s, value=%s, "
                  "old_value=%s" % (key, value, ref.old_value))
        if debug:
            pp.pprint(node)
    elif key < node.key:
        node.left = insert_random(node.left, key, value, ref, debug=debug)
        if ref.is_new:
            node.size += 1
    elif key > node.key:
        node.right = insert_random(node.right, key, value, ref, debug=debug)
        if ref.is_new:
            node.size += 1
    else:
        if debug:
            print("insert_random(found old_value): node.key=%s, "
                  "node.value=%s, old_value=%s" % (key, value, ref.old_value))
        ref.old_value = node.value
        assert node.key == key
        if debug:
            print("insert_random(registered old_value): node.key=%s, "
                  "node.value=%s, old_value=%s" % (key, value, ref.old_value))

    if debug:
        print("insert_random(end): key=%s, value=%s, old_value=%s"
              % (key, value, ref.old_value))
    if debug:
        pp.pprint(node)
    return node


def insert_at_root(node, key, value, ref, debug=False):
    if debug:
        print("insert_at_root(begin): key=%s, value=%s, old_value=%s"
              % (key, value, ref.old_value))
    if debug:
        pp.pprint(node)
    if node is None:
        if debug:
            print("insert_at_root(exit node was None): key=%s, value=%s, "
                  "old_value=%s" % (key, value, ref.old_value))
        ref.is_new = True
        return Node(key, value)
    if key < node.key:
        if debug:
            print("insert_at_root(recursing on left): key=%s, value=%s, "
                  "old_value=%s" % (key, value, ref.old_value))
        node.left = insert_at_root(node.left, key, value, ref, debug=debug)
        if ref.is_new:
            node.size += 1
        node = rotate_right(node, ref, debug)
    elif key > node.key:
        if debug:
            print("insert_at_root(recursing on right): key=%s, value=%s, "
                  "old_value=%s" % (key, value, ref.old_value))
        node.right = insert_at_root(node.right, key, value, ref, debug=debug)
        if ref.is_new:
            node.size += 1
        node = rotate_left(node, ref, debug=debug)
    else:
        if debug:
            print("insert_at_root(set): node.key=%s, node.value=%s, "
                  "old_value=%s" % (key, value, ref.old_value))
        ref.old_value = node.value
        node.key, node.value = key, value
    if debug:
        print("insert_at_root(end): key=%s, value=%s, old_value=%s"
              % (key, value, ref.old_value))
    if debug:
        pp.pprint(node)
    return node


def rotate_left(node, ref, debug=False):
    if debug:
        print("rotate_left(begin): node->")
    if debug:
        pp.pprint(node)
    node.size, node.right.size = (size(node) - right_size(node.right) - 1,
                                  node.size)
    x = node.right
    node.right = x.left
    x.left = node
    if debug:
        print("rotate_left(end): x->")
    if debug:
        pp.pprint(x)
    return x


def rotate_right(node, ref, debug=False):
    if debug:
        print("rotate_right(begin): node->")
    if debug:
        pp.pprint(node)
    node.size, node.left.size = (size(node) - left_size(node.left) - 1,
                                 node.size)
    x = node.left
    node.left = x.right
    x.right = node
    if debug:
        print("rotate_right(end): x->")
    if debug:
        pp.pprint(x)
    return x


def remove(tree, key):
    if tree is None or tree.root is None or key is None:
        return
    ref = Ref()
    ref.rem_node = None
    tree.root = remove_r(tree.root, key, ref)
    return ref.rem_node.value if ref.rem_node else None


def remove_r(node, key, ref):
    if node is None:
        return
    if key < node.key:
        node.left = remove_r(node.left, key, ref)
        if ref.rem_node is not None:
            node.size -= 1
    elif key > node.key:
        node.right = remove_r(node.right, key, ref)
        if ref.rem_node is not None:
            node.size -= 1
    else:
        ref.rem_node = node
        node = join_lr(node.left, node.right)
    return node


def join_lr(left, right):
    if left is None:
        return right
    if right is None:
        return left
    n = left.size + right.size
    if random.random() * n < (1.0 * left.size):
        left.right = join_lr(left.right, right)
        left.size = n
        return left
    else:
        right.left = join_lr(left, right.left)
        right.size = n
        return right


def min_key(tree):
    if tree is None:
        return None
    curr = tree.root
    while curr is not None and curr.left is not None:
        curr = curr.left
    return curr.key if curr else None


def max_key(tree):
    if tree is None:
        return None
    curr = tree.root
    while curr is not None and curr.right is not None:
        curr = curr.right
    return curr.key if curr else None


def size(node):
    return node.size if node else 0


def left_size(node):
    return node.left.size if (node and node.left) else 0


def right_size(node):
    return node.right.size if (node and node.right) else 0


def verify_size(x, debug=True):
    if isinstance(x, Tree):
        x = x.root
    if x is None:
        return
    calc_size = size_calc(x)
    if (x is not None and size(x) != (1 + left_size(x) + right_size(x)) or
            size(x) != calc_size):
        if debug:
            print("Invalid Size:\nnode (calc_size=%d):" % (calc_size,))
            pprint(x)
        else:
            raise Exception("Invalid Size: (calc_size=%d, node.size=%d)"
                            % (calc_size, x.size))
    verify_size(x.left if x else None)
    verify_size(x.right if x else None)


def height(x):
    if isinstance(x, Tree):
        x = x.root
    if x is None:
        return 0
    return 1 + max(height(x.left), height(x.right))


def size_calc(node):
    if node is None:
        return 0
    return (1 + (size_calc(node.left) if node.left else 0) +
            (size_calc(node.right) if node.right else 0))


def seed(tree, n, low=0, high=None, unique=False, debug=False):
    if high is None:
        high = 100 * n

    def next():
        return random.randint(low, high)
    keys = set([])
    for i in range(n):
        key = next()
        if unique:
            while key in keys:
                key = next()
        keys.add(key)
        new_val = next()
        put(tree, key, new_val, debug=debug)

tree = Tree()


def f(tree, n=100, debug=False):
    for i in range(n):
        put(tree, i, random.randint(0, n * 10), debug=debug)
        size_c = size_calc(tree.root)
        if tree.root.size != size_c:
            print("ERROR: tree.root.size=%d, size_calc(tree.root)=%d"
                  % (tree.root.size, size_c))
            break


def stress_test_seed(n=1000 * 1000, check_min_max=True, ordered=False):
    tree = Tree()
    curr_min, curr_max = None, None
    for i in xrange(n):
        if ordered:
            k, v = i, i * 2
        else:
            k, v = random.randint(0, n), random.randint(0, n)
        if curr_min is None or k < curr_min:
            curr_min = k
        if curr_max is None or k > curr_max:
            curr_max = k
        put(tree, k, v)
        if check_min_max:
            assert min_key(tree) == curr_min
            assert max_key(tree) == curr_max
        if i > 0 and i % 100000 == 0:   # check size every 100,000
            print("%6d %6d: verifying size of %d"
                  % (i, height(tree.root), tree.root.size))
            verify_size(tree, debug=False)
        elif i > 0 and i % 10000 == 0:  # print status
            print("%6d %6d: size is %d"
                  % (i, height(tree.root), tree.root.size))
    return tree


def stress_test_unseed_minmax(tree):
    curr_min, curr_max = min_key(tree), max_key(tree)
    prev_min, prev_max = None, None
    size = tree.root.size
    while not tree.is_empty():
        if size % 100000 == 0:
            print("%6d %6d: verifying size" % (size, height(tree.root)))
            verify_size(tree.root)
        elif size % 10000 == 0:
            print("size, height = %s, %s" % (size, height(tree.root)))
        assert size == tree.root.size
        if random.choice((True, False)):
            prev_min = curr_min
            assert remove(tree, curr_min) is not None
            if not tree.is_empty():
                curr_min = min_key(tree)
                assert (curr_min > prev_min,
                        "curr_min=%s, prev_min=%s" % (curr_min, prev_min))
        else:
            prev_max = curr_max
            assert remove(tree, curr_max) is not None
            if not tree.is_empty():
                curr_max = max_key(tree)
                assert (curr_max < prev_max, "curr_max=%s, prev_max=%s"
                        % (curr_max, prev_max))
        # randomly try to remove a non-existent key as well
        # (all keys are non-negative)
        assert remove(tree, (curr_max + 1) * -1) is None
        assert (tree.root.size == size,
                "size after removing non-existent item '%s' should "
                "be same as before '%s'." % (tree.root.size, size))
        size -= 1
    assert size == 0
    assert tree.root is None
    print("last (min, max) = (%s, %s)" % (curr_min, curr_max))


pickle_path = 'tree.pickle'


def write_tree(tree, path=pickle_path):
    f = open(path, 'wb')
    try:
        dump(tree, f, -1)
    finally:
        f.close()


def read_tree(path=pickle_path):
    f = open(path, 'rb')
    try:
        tree = load(f)
    finally:
        f.close()
    return tree

t = Tree()
r, w, s = read_tree, write_tree, seed
unpop, pop = stress_test_unseed_minmax, stress_test_seed
