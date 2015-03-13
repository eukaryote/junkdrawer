import math
import operator
import sets
import functools

"""A module providing some basic linear algebra operations.

The functions cover the standard basic operations on vectors and matrices.
If you are looking for an efficient and complete linear algebra module,
this isn't it. This module is intended just as a simple (no install,
no dependencies) way of double-checking some of the more tedious
linear algebra stuff as I worked my way through a linear algebra text.

The tests embedded in the docstring of each function shows basic usage of the
function, and all tests can be run by executing:

python linearalgebra.py

No output means success. If you want the output to display what is being
tested, run:

python linearalgebra.py -v

Some useful math functions and constants are re-exported from the standard
Python math module, as a convenience for interactive scripting. These include
e, pi, sqrt, cos, sin, tan, acos, asin, and atan.

Conventions for function parameters:
  * u and v always refer to a vector;
  * s and c always refer to a scalar;
  * A, B, and C always refer to a matrix;
  * m, n, r always refer to a scalar that is the dimension of a matrix
    (e.g., m = 3, n = 2 for a 3 x 2 or m x n matrix);
  * x may be either a vector or a scalar;
  * any of these may be postfixed by an integer, and is of the same type
    as the unpostfixed variable name (e.g., m2 is a scalar)."""


# We re-export these from the math module for convenience.
degrees = math.degrees
radians = math.radians
e = math.e
pi = math.pi
sqrt = math.sqrt
cos = math.cos
sin = math.sin
tan = math.tan
acos = math.acos
asin = math.asin
atan = math.atan

# The value we use for determining whether a float is equal to an
# int: if the difference is less than epsilon, we deem them equal.
epsilon = 0.000000000000001


class LAValueError(ValueError):
    pass


class InvalidVectorException(LAValueError):
    pass


class IncompatibleVectorException(LAValueError):
    pass


class InvalidMatrixException(LAValueError):
    pass


class IncompatibleMatrixException(LAValueError):
    pass


# Some simple decorators for verifying arguments to functions below,
# in order to provide friendlier error messages.


def check_vector_same_size(index1, index2):
    """ Decorates a function such that an exception is raised if the
    arg at index1 or index 2 is not a vector or if they do not have
    the same size, and otherwise executes the function as usual. """
    def decorator(func):
        @functools.wraps(func)
        def _decorator(*args):
            if not is_vector(args[index1]):
                msg = "1st arg to check_vector_same_size is not a vector"
                raise InvalidVectorException(msg)
            elif not is_vector(args[index2]):
                msg = "2nd arg to check_vector_same_size is not a vector"
                raise InvalidVectorException(msg)
            if len(args[index1]) != len(args[index2]):
                raise IncompatibleVectorException(
                    "Vectors must be of equal size, not %d and %d."
                    % (len(args[index1]), len(args[index2])))
            return func(*args)
        return _decorator
    return decorator


# Check that two matrices have the same number of rows and columns.
def check_matrix_same_size(index1, index2):
    """ Decorates a function such that an exception is raised if the
    arg at index1 or index2 is not a matrix or if they to not have
    the same dimensions, and otherwise executes the function as usual. """
    def decorator(func):
        @functools.wraps(func)
        def _decorator(*args):
            (m1, n1) = matrix_dimensions(args[index1])
            (m2, n2) = matrix_dimensions(args[index2])
            if m1 != m2 or n1 != n2:
                msg = ("Matrices must have same dimensions. Matrix 1 is "
                       "%d x %d, but matrix 2 is %d x %d.")
                raise IncompatibleMatrixException(msg % (m1, n1, m2, n2))
            return func(*args)
        return _decorator
    return decorator


# Check that one or more args of a function is a scalar.
def check_scalar(*arg_indices):
    """ Decorates a function such that an exception is raised if the arg at
    any of the supplied indices is not a scalar, and otherwise executes
    the function as usual."""
    def decorator(func):
        @functools.wraps(func)
        def _decorator(*args):
            for arg_index in arg_indices:
                arg = args[arg_index]
                if not is_scalar(arg):
                    msg = "Arg at index %s is not a scalar: %s"
                    raise LAValueError(msg % (arg_index, arg))
            return func(*args)
        return _decorator
    return decorator


# Check that one or more args is a vector.
def check_vector(*arg_indices):
    """ Decorates a function such that an exception is raised if the vector
    arg at any of the supplied indices is not actually a vector, and otherwise
    executes the function as usual. """
    def decorator(func):
        @functools.wraps(func)
        def _decorator(*args):
            for arg_index in arg_indices:
                u = args[arg_index]
                if not is_vector(u):
                    msg = "Arg should be a vector: %s" % repr(u)
                    raise InvalidVectorException(msg)
            return func(*args)
        return _decorator
    return decorator


# Check that one or more args is a matrix.
def check_matrix(*arg_indices):
    """ Decorates a function such that an exception is raised if the matrix
    arg at any of the supplied indices is not a matrix, and otherwise executes
    the function as usual. """
    def decorator(func):
        @functools.wraps(func)
        def _decorator(*args):
            for arg_index in arg_indices:
                a = args[arg_index]
                if not is_matrix(a):
                    raise InvalidMatrixException("Arg is not a matrix: %s"
                                                 % repr(a))
            return func(*args)
        return _decorator
    return decorator


# Check that the number of columns of the first matrix equals number of rows
# of the second matrix.
def check_matrix_multipliable(index1, index2):
    """ Decorates a function such that an exception is raised if
    the multiplication of matrices (args[index1], args[index2]) is not
    permitted due to incompatible size. I.e., if the number of the columns
    in the first matrix is not equal to the number of rows in the second. """
    def decorator(func):
        @functools.wraps(func)
        def _decorator(*args):
            (m1, n1) = matrix_dimensions(args[index1])
            (m2, n2) = matrix_dimensions(args[index2])
            if n1 != m2:
                msg = ("Matrices are not size-compatible. Matrix 1 has %s "
                       "column(s), but matrix 2 has %s row(s) instead of %s")
                raise IncompatibleMatrixException(msg % (n1, m2, n1))
            return func(*args)
        return _decorator
    return decorator


# Actual functions defined below here.


def is_matrix(ma):
    """
    Determine whether the given arg is a matrix, which must
    be a rectangular array of numbers, represented as a list/tuple of
    list/tuple elements, each of which is a vector of equal size.
    >>> is_matrix([])
    True
    >>> is_matrix([[]])
    True
    >>> is_matrix([1,2])
    False
    >>> is_matrix([[1,2], (3,4)])
    True
    >>> is_matrix([[1,2], [3,4,5]])
    False
    >>> is_matrix([[1,2], ['0', 1]])
    False
    >>> is_matrix([[.5, -1, 9], [4, 3, 19], [3, 6, 8], [0, 0, 1]])
    True
    """
    if not is_vector_type(ma) or not all_true(ma, is_vector_type):
        return False
    if len(ma) == 0:
        return True
    n = len(ma[0])
    return all_true(ma, lambda row: is_vector(row) and len(row) == n)


@check_matrix(0)
def matrix_dimensions(ma):
    """
    Calculates the dimensions of the given matrix, returning a pair consisting
    of the number of rows and the number of columns, raising an exception if
    any of the rows of the matrix have a different number of elements.

    >>> matrix_dimensions([])
    (0, 0)
    >>> matrix_dimensions([[1,2,3]])
    (1, 3)
    >>> matrix_dimensions([[1], [2], [3]])
    (3, 1)
    >>> matrix_dimensions([[1, 2], [1, 2, 3]])
    Traceback (most recent call last):
      ...
    InvalidMatrixException: Arg is not a matrix: [[1, 2], [1, 2, 3]]
    """
    m = len(ma)
    if m == 0:
        return (0, 0)
    n = len(ma[0])
    for (i, row) in enumerate(ma):
        l = len(row)
        if n != l:
            msg = ("Matrix has rows of different length: row 0 has "
                   "%d element(s) and row %d has %d element(s)." % (n, i, l))
            raise InvalidMatrixException(msg)
    return (m, n)


@check_matrix(0)
def matrix_is_square(ma):
    """
    Determine whether the given matrix is a square matrix, with the same
    number of rows and columns.

    >>> matrix_is_square([])
    True
    >>> matrix_is_square([[]])
    False
    >>> matrix_is_square([[1,1], [2,2], [3,3]])
    False
    >>> matrix_is_square([[1,2,3], [4,5,6], [7,8,9]])
    True
    >>> matrix_is_square([[1], [1,2]])
    Traceback (most recent call last):
      ...
    InvalidMatrixException: Arg is not a matrix: [[1], [1, 2]]
    """
    (m, n) = matrix_dimensions(ma)
    return m == n


@check_matrix(0)
def matrix_is_diagonal(ma):
    """
    Determine whether the given matrix is a diagonal matrix -- i.e., a
    square matrix with all nondiagonal entries equal to 0.

    >>> matrix_is_diagonal([])
    True
    >>> matrix_is_diagonal([[0]])
    True
    >>> matrix_is_diagonal([[0, 0], [0, 0], [0, 0]])
    False
    >>> matrix_is_diagonal([[1, 0], [0, 2]])
    True
    >>> matrix_is_diagonal([[1, 0], [1, 0]])
    False
    """
    if not matrix_is_square(ma):
        return False
    for (i, row) in enumerate(ma):
        for (j, elem) in enumerate(row):
            if i != j and elem != 0:
                return False
    return True


@check_matrix(0)
def matrix_is_scalar(ma):
    """
    Determine whether the given matrix is a scalar matrix -- i.e., a diagonal
    matrix with all diagonal entries equal to each other.

    >>> matrix_is_scalar([])
    True
    >>> matrix_is_scalar([[2]])
    True
    >>> matrix_is_scalar([[3, 0], [0, 3]])
    True
    >>> matrix_is_scalar([[3, 0], [1, 3]])
    False
    """
    if not matrix_is_square(ma):
        return False
    elif len(ma) == 0:
        return True
    diag_val = ma[0][0]
    for (i, row) in enumerate(ma):
        for (j, elem) in enumerate(row):
            if (i != j and elem != 0) or (i == j and elem != diag_val):
                return False
    return True


@check_matrix(0)
def matrix_is_identity(ma):
    """
    Determine whether the given matrix is an identity matrix -- i.e.,
    a non-empty scalar matrix with all diagonal entries equal to 1.

    >>> matrix_is_identity([])
    False
    >>> matrix_is_identity([[0]])
    False
    >>> matrix_is_identity([[1]])
    True
    >>> matrix_is_identity([[1, 1], [1, 1]])
    False
    >>> matrix_is_identity([[1, 0], [0, 1]])
    True
    >>> matrix_is_identity([[1, 0], [0, 1], [0, 0]])
    False
    >>> matrix_is_identity([[2, 0], [0, 2]])
    False
    """
    if not matrix_is_square(ma):
        return False
    elif len(ma) == 0:
        return False
    for (i, row) in enumerate(ma):
        for (j, elem) in enumerate(row):
            if (i != j and elem != 0) or (i == j and elem != 1):
                return False
    return True


@check_matrix(0)
def matrix_is_symmetric(ma):
    """
    Determine whether the given matrix is symmetric -- i.e., whether it is
    equal to its own transpose.

    >>> matrix_is_symmetric([[1, 0], [0, 1]])
    True
    >>> matrix_is_symmetric([[0, 1], [1, 0]])
    True
    >>> matrix_is_symmetric([[1, 2], [2, 0]])
    True
    >>> matrix_is_symmetric([[1, 2], [1, 2]])
    False
    >>> matrix_is_symmetric([[1, 3, 2], [3, 5, 0], [2, 0, 4]])
    True
    """
    return matrix_equal(ma, matrix_transpose(ma))


def matrix_pairwise_op(ma, mb, func):
    """
    Helper function for matrix_plus and matrix_minus.
    """
    (m, n) = matrix_dimensions(ma)
    mc = [None] * m
    for i in range(m):
        row = [None] * n
        for j in range(n):
            row[j] = func(ma[i][j], mb[i][j])
        mc[i] = row
    return mc


@check_matrix_same_size(0, 1)
def matrix_plus(ma, mb):
    """
    Add the given matrices, which must have the same number of rows and
    columns.

    >>> matrix_plus([[1, 2], [3, 4]], [[4, 3], [2, 1]])
    [[5, 5], [5, 5]]
    >>> matrix_plus([[1,2]], [[3, 4]]), matrix_plus([[1,2]], [[3, 4]])[0] == vector_plus([1,2], [3,4])
    ([[4, 6]], True)
    >>> matrix_plus([[1]], [[1, 2]])
    Traceback (most recent call last):
      ...
    IncompatibleMatrixException: Matrices must have same dimensions. Matrix 1 is 1 x 1, but matrix 2 is 1 x 2.
    """
    return matrix_pairwise_op(ma, mb, operator.add)


@check_matrix_same_size(0, 1)
def matrix_minus(ma, mb):
    """
    Subtract the second matrix from the first, both of which must have the
    same number of rows and columns.

    >>> matrix_minus([[3, 4], [1, 2]], [[1, 1], [1, 1]])
    [[2, 3], [0, 1]]
    >>> matrix_minus([[1,2]], [[3, 4]]), matrix_minus([[1,2]], [[3, 4]])[0] == vector_minus([1,2], [3,4])
    ([[-2, -2]], True)
    >>> matrix_minus([[1]], [[1, 2]])
    Traceback (most recent call last):
      ...
    IncompatibleMatrixException: Matrices must have same dimensions. Matrix 1 is 1 x 1, but matrix 2 is 1 x 2.
    """
    return matrix_pairwise_op(ma, mb, operator.sub)


@check_scalar(0)
@check_matrix(1)
def matrix_times(s, ma):
    """
    Multiply the matrix A by the scalar s.

    >>> matrix_times(2, [[0,1], [1, 0]])
    [[0, 2], [2, 0]]
    >>> matrix_times(-1, [[1,2,3,4]])
    [[-1, -2, -3, -4]]
    >>> matrix_times(3, [[]])
    [[]]
    >>> matrix_times(1, [])
    []
    >>> matrix_times(3, [[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]])
    [[3, 6, 9], [12, 15, 18], [21, 24, 27], [30, 33, 36]]
    """
    return [[s * elem for elem in row] for row in ma]


@check_matrix(0)
def matrix_negative(ma):
    """
    Return the negative of the given matrix, or the matrix multiplied
    by scalar -1.

    >>> matrix_negative([])
    []
    >>> matrix_negative([[]])
    [[]]
    >>> matrix_negative(((-1, 2), (2, -3)))
    [[1, -2], [-2, 3]]
    """
    return matrix_times(-1, ma)


@check_matrix(0)
def matrix_transpose(ma):
    """
    Generate the transpose of the given m x n matrix, which is the n x m
    matrix with where each (i,j) element of the original matrix is the (j,i)
    element of the new matrix.

    >>> matrix_transpose([[1, 2], [3, 4], [5, 6]])
    [[1, 3, 5], [2, 4, 6]]
    >>> matrix_transpose([])
    []
    >>> matrix_transpose([[]])
    []
    >>> matrix_transpose([[1,2,3], [4,5,6], [7,8,9]])
    [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    >>> matrix_transpose(matrix_transpose([[1,2,3], [4,5,6], [7,8,9]]))
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> matrix_transpose([[1,2,3]])
    [[1], [2], [3]]
    """
    (m, n) = matrix_dimensions(ma)
    c = [[None] * m for i in range(n)]
    for i in range(m):
        for j in range(n):
            c[j][i] = ma[i][j]
    return c


@check_matrix_multipliable(0, 1)
@check_matrix(0, 1)
def matrix_product(ma, mb):
    """
    Calculate the product of matrices A and B, where A must have the
    same number of columns and B has rows. The result for A of size m x n
    and B of size n x r is an m x r matrix.

    >>> matrix_product([[1,1], [1,1]], [[1,1], [1,1]])
    [[2, 2], [2, 2]]
    >>> matrix_product([], [])
    []
    >>> matrix_product([[1, 3, -1], [-2, -1, 1]], [[-4, 0, 3, -1], [5, -2, -1, 1], [-1, 2, 0, 6]])
    [[12, -8, 0, -4], [2, 4, -5, 7]]
    """
    (m, n) = matrix_dimensions(ma)
    (n, r) = matrix_dimensions(mb)
    mc = [[None] * r for i in range(m)]
    for i in range(m):
        for j in range(r):
            mc[i][j] = vector_product(ma[i], [row[j] for row in mb])
    return mc


def scalar_equal(s1, s2, eps=epsilon):
    """
    Determine whether the two scalars are equal to accuracy of epsilon.

    >>> scalar_equal(0.9000000000000002, 0.9000000000000001)
    True
    >>> scalar_equal(1, 1)
    True
    >>> scalar_equal(1, 1.0)
    True
    >>> scalar_equal(1.0, 1.00000001)
    False
    """
    return abs(s1 - s2) < eps


@check_vector_same_size(0, 1)
def vector_equal(u, v):
    """
    Determine whether the two vectors are equal by determining if the
    pairwise components are equal to accuracy of epsilon.

    >>> vector_equal([2], [2])
    True
    >>> vector_equal([1.0, 0.9000000000000002], [1, 0.9000000000000001])
    True
    """
    return all_true(map(lambda (x, y): scalar_equal(x, y), zip(u, v)))


@check_matrix(0, 1)
def matrix_equal(ma, mb):
    """
    Determine whether the two matrices are equal by determining if
    the corresponding components are equal to accuracy of epsilon.

    >>> matrix_equal([], [])
    True
    >>> matrix_equal([[1, 2, 3], [3.9000000000000001, 2, 1]], [[1, 2, 3], [3.9, 2, 1]])
    True
    """
    (m1, n1) = matrix_dimensions(ma)
    (m2, n2) = matrix_dimensions(mb)
    if m1 != m2 or n1 != n2:
        return False
    for i in range(m1):
        for j in range(n1):
            if not scalar_equal(ma[i][j], mb[i][j]):
                return False
    return True


def vector_zero(x):
    """
    Create a zero vector with same size as the given vector, or
    having as many elements as the given int.

    >>> vector_zero(3)
    [0, 0, 0]
    >>> vector_zero([1,2,3,4])
    [0, 0, 0, 0]
    >>> vector_zero([])
    []
    """
    if isinstance(x, int):
        return [0] * x
    elif not isinstance(x, (list, tuple)):
        raise LAValueError("Arg should be a vector or int, not: %s" % repr(x))
    else:
        return [0 for n in x]


@check_vector(0)
def vector_unit_length(v):
    """
    Create a unit-length vector in direction of v.

    >>> vector_unit_length([3,3])
    [0.7071067811865476, 0.7071067811865476]
    """
    return vector_times(1.0 / vector_norm(v), v)


@check_vector(1)
def vector_times(s, v):
    """
    Multiply the vector by the given scalar.

    >>> vector_times(3, [1,2])
    [3, 6]
    >>> vector_times(5, [4,-2,7])
    [20, -10, 35]
    >>> vector_times(0, [1,2,3])
    [0, 0, 0]
     """
    return map(lambda x: s * x, v)


def vector_pairwise_op(u, v, func):
    """
    A helper function that applies the given 2-arg func to
    the pairwise elements of the two vectors.
    """
    return map(lambda (x, y): func(x, y), zip(u, v))


@check_vector_same_size(0, 1)
def vector_plus(u, v):
    """
    Calculate the vector resulting from the addition of the two given vectors.

    >>> vector_plus([1,2], [3,4])
    [4, 6]
    >>> vector_plus([0.5, 1], [2.5, -1])
    [3.0, 0]
    """
    return vector_pairwise_op(u, v, operator.add)


@check_vector_same_size(0, 1)
def vector_minus(u, v):
    """
    Subtract the second vector from the first vector.

    >>> vector_minus([2], [-3])
    [5]
    >>> vector_minus([1,2,3], [2,3,4])
    [-1, -1, -1]
    """
    return vector_pairwise_op(u, v, operator.sub)


@check_vector_same_size(0, 1)
def vector_product(u, v):
    """
    Calculate the dot product of the given vectors, which is defined
    as the sum of the pairwise products of the vectors.

    >>> vector_product([0,0], [0,1])
    0
    >>> vector_product([1,2,-3], [-3,5,2])
    1
    """
    return sum(vector_pairwise_op(u, v, operator.mul))


@check_vector(0)
def vector_norm(v):
    """
    Calculate the length, or norm, of the vector, which
    is defined to be the square root of the sum of the squares
    of the components of the vector.

    >>> vector_norm([0,1])
    1.0
    >>> vector_norm([1,1]), scalar_equal(vector_norm([1,1]), sqrt(2))
    (1.4142135623730951, True)
    >>> vector_norm([2,-1,3]), scalar_equal(vector_norm([2,-1,3]), sqrt(14))
    (3.7416573867739413, True)
    >>> vector_norm([sqrt(2), -1, 1])
    2.0
    """
    return math.sqrt(sum(map(lambda x: x * x, v)))


@check_vector_same_size(0, 1)
def vector_distance(u, v):
    """
    Calculate the distance between the two vectors, which
    is defined to be the norm of the difference between the
    vectors.
    >>> vector_distance([sqrt(2), 1, -1], [0, 2, -2])
    2.0
    >>> vector_distance([0,1], [1,0])
    1.4142135623730951
    >>> vector_distance([-1,2], [3,1])
    4.123105625617661
    """
    return vector_norm(vector_minus(u, v))


@check_vector_same_size(0, 1)
def vector_is_orthogonal(u, v):
    """
    Determine whether the two vectors are orthogonal, which
    is defined by whether the dot product is 0.

    >>> vector_is_orthogonal([0,1], [1,0])
    True
    >>> vector_is_orthogonal([2,-1,1], [1,-2,-1])
    False
    >>> vector_is_orthogonal([1,1,-2], [3,1,2])
    True
    """
    return abs(vector_product(u, v)) < epsilon


@check_vector_same_size(0, 1)
def vector_angle(u, v):
    """
    Determine the angle between the two vectors, in radians.

    >>> vector_angle([0,1,1], [1,0,1]), scalar_equal(vector_angle([0,1,1], [1,0,1]), pi/3)
    (1.0471975511965979, True)
    >>> vector_angle([0.9, 2.1, 1.2], [-4.5, 2.6, -0.8])
    1.5376292299388497
    """
    return math.acos(vector_product(u, v) / (vector_norm(u) * vector_norm(v)))


@check_vector_same_size(0, 1)
def vector_project(u, v):
    """
    Calculate the projection of v onto u.

    >>> vector_project([2,1], [-1, 3]), vector_equal(vector_project([2,1], [-1, 3]), [2.0/5, 1.0/5])
    ([0.4, 0.2], True)
    >>> vector_project([0,0,1], [1,2,3]), vector_equal(vector_project( [0,0,1], [1,2,3]), [0,0,3])
    ([0.0, 0.0, 3.0], True)
    """
    return vector_times(float(vector_product(u, v)) / vector_product(u, u), u)

# Don't include complex, because python can be built without support.
__NUMBER_TYPES = sets.Set([int, float, long])


def is_vector_type(u):
    """ Determine whether arg is a vector type (list or tuple). """
    return isinstance(u, (list, tuple))


def is_vector(u):
    """
    Determine whether the arg is a vector, or a list or tuple of numbers.

    >>> is_vector('')
    False
    >>> is_vector([])
    True
    >>> is_vector(())
    True
    >>> is_vector((1,))
    True
    >>> is_vector([1])
    True
    >>> is_vector([1,2,3,4])
    True
    >>> is_vector((1,2,3))
    True
    >>> is_vector([1, 0.5, -9L])
    True
    >>> is_vector([1, 2, "3"])
    False
    >>> is_vector([[0]])
    False
    >>> is_vector([[1,2]])
    False
    """
    return is_vector_type(u) and all_true(u, is_scalar)


def is_scalar(s):
    """
    Determine whether s is a scalar, which is either a float, int,
    or long. The integral values 0 and 1 may also be given as
    False and True, respectively.

    >>> is_scalar(0)
    True
    >>> is_scalar(True)
    True
    >>> is_scalar(-9.2)
    True
    >>> is_scalar(100L)
    True
    >>> is_scalar((1,2))
    False
    """
    return isinstance(s, (int, float, long))


def all_true(lst, test=bool):
    """
    Determine if all items in list evaluate to True using the optional
    test function, which defaults to bool.

    >>> all_true([])
    True
    >>> all_true([1,0])
    False
    >>> all_true([True, 1])
    True
    >>> all_true([True, True, False])
    False
    >>> all_true([1,2,3], lambda s: s % 2 == 0)
    False
    >>> all_true([2,4,6], lambda s: s % 2 == 0)
    True
    """
    for res in lst:
        if not test(res):
            return False
    return True


def test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()
