
:mod:`linearalgebra` -- Basic functions on vectors and matrices.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: linearalgebra
   :platform: Unix, Windows
   :synopsis: Basic functions for manipulating vectors and matrices.
.. moduleauthor:: Calvin Smith

Overview
========

The :mod:`linearalgebra` module provides some basic functions on
vectors and matrices.

The functions cover the standard basic operations on vectors and matrices.
If you are looking for an efficient and complete linear algebra module,
this isn't it. (Try NumPy instead.)

This module is intended just as a simple (no install, no dependencies)
way of double-checking some of the more tedious linear algebra stuff
as I worked my way through a linear algebra text.

The tests embedded in the docstring of each function shows basic usage of the
function, and all tests can be run by executing:

`python linearalgebra.py`

No output means success. If you want the output to display what is being
tested, run:

`python linearalgebra.py -v`

Some useful math functions and constants are re-exported from the standard
Python math module, as a convenience for interactive scripting. These include
`e`, `pi`, `sqrt`, `cos`, `sin`, `tan`, `acos`, `asin`, and `atan`.

Function Parameter Conventions
==============================

The following conventions are observed for function arguments:

  * *u* and *v* always refer to a vector;
  * *s* and *c* always refers to a scalar;
  * *ma*, *mb*, and *mc* always refer to a matrix;
  * *m*, *n*, *r* always refer to a scalar that is the dimension of a matrix
    (e.g., m = 3, n = 2 for a 3 x 2 or m x n matrix);
  * *x* may be either a vector or a scalar;
  * any of these may be suffixed with an integer, and has the same type
    as the unsuffixed variable name (e.g., *m1* is a scalar and *bm7* is
    a matrix).

Scalar Functions
================

.. autofunction:: is_scalar(s)

.. autofunction:: scalar_equal(s1, s2, eps=epsilon)

Vector Functions
================

.. autofunction:: is_vector(u)

.. autofunction:: vector_equal(u, v)

.. autofunction:: vector_zero(x)

.. autofunction:: vector_unit(v)

.. autofunction:: vector_times(s, v)

.. autofunction:: vector_plus(u, v)

.. autofunction:: vector_minus(u, v)

.. autofunction:: vector_product(u, v)

.. autofunction:: vector_norm(v)

.. autofunction:: vector_distance(u, v)

.. autofunction:: vector_is_orthogonal(u, v)

.. autofunction:: vector_angle(u, v)

.. autofunction:: vector_project(u, v)

Matrix Functions
================

.. autofunction:: is_matrix(a)

.. autofunction:: matrix_is_square(a)

.. autofunction:: matrix_is_diagonal(a)

.. autofunction:: matrix_is_scalar(a)

.. autofunction:: matrix_is_identity(a)

.. autofunction:: matrix_is_symmetric(a)

.. autofunction:: matrix_equal(a, b)

.. autofunction:: matrix_dimensions(a)

.. autofunction:: matrix_times(s, a)

.. autofunction:: matrix_plus(a, b)

.. autofunction:: matrix_minus(a, b)

.. autofunction:: matrix_negative(a)

.. autofunction:: matrix_product(a, b)

.. autofunction:: matrix_transpose(a)

