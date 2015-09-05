"""
Scratchpad while reading Cook's "On Understanding Data Abstraction, Revisted".
"""

from collections import namedtuple


class Namespace(object):
    pass


# ADT formulation of IntSet (analogous to algebraic structure in math)
ADT = Namespace()
ADT.empty = object()
ADT.ins = namedtuple('ains', ['head', 'tail'])
ADT.insert = lambda s, i: ADT.ins(i, s) if not ADT.contains(s, i) else s
ADT.isEmpty = lambda s: s is ADT.empty
ADT.contains = (lambda s, i: False if ADT.isEmpty(s)
                                   else (True if i == s.head
                                              else ADT.contains(s.tail, i)))
ADT.union = (lambda s1, s2: s2 if ADT.isEmpty(s1)
                               else ADT.insert(ADT.union(s1.tail, s2),
                                               s1.head))


def run_adt():
    a = ADT.insert(ADT.empty, 1)
    b = ADT.insert(a, 3)
    assert ADT.isEmpty(ADT.empty)
    assert not ADT.isEmpty(a)
    assert ADT.contains(a, 1)
    assert not ADT.contains(a, 3)
    assert ADT.contains(b, 1)
    assert ADT.contains(b, 3)
    assert not ADT.contains(b, 2)


# object formulation of IntSet (analogous to characteristic function in math)
OBJ = Namespace()
OBJ.empty = lambda i: False
OBJ.insert = lambda s, n: (lambda i: s(i) if i != n else True)
OBJ.union = lambda s1, s2: (lambda i: s1(i) or s2(i))


def run_object():
    a = OBJ.insert(OBJ.empty, 1)
    b = OBJ.insert(a, 3)
    assert a(1)
    assert not a(3)
    assert b(1)
    assert b(3)
    assert not b(2)


def main():
    run_adt()
    run_object()


if __name__ == '__main__':
    main()
