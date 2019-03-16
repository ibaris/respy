# -*- coding: utf-8 -*-
# cython: cdivision=True
"""
Created on 15.03.2019 by Ismail Baris
"""
import numpy as np
cimport numpy as np
import sympy

cdef tuple bin_decompose_expr(object expr):
    """
    Decompose a sympy expression to value and units.
    
    Parameters
    ----------
    expr : sympy expression
        A sympy expression.
        
    Returns
    -------
    tuple (DTYPE_SCALAR value, object unit)
    """
    cdef:
        Py_ssize_t i
        object unit_obj
        tuple unit

    if 'Pow' in str(type(expr)):
        value = 1
        unit_obj = expr

    elif 'Mul' in str(type(expr)):
        value = expr.args[0]

        try:
            value = float(value)
            unit = expr.args[1:]

            if len(unit) == 1:
                unit_obj = unit[0]
            else:
                unit_obj = unit[0]

                for i in range(1, len(unit)):
                    unit_obj *= unit[i]

        except TypeError:
            value = 1
            unit_obj = expr

    else:
        raise TypeError("Data type {0} not understood.".format(str(expr)))

    return value, unit_obj

cdef tuple bin_decompose_expr_array(value):
    """
    Decompose a array with sympy expressions to value and units.
    
    Parameters
    ----------
    value : numpy.ndarray
        An array with sympy expressions.
        
    Returns
    -------
    tuple (DTYPE_ARRAY value, object unit)
    """

    cdef:
        tuple shape
        Py_ssize_t i

    shape = value.shape
    value_flatten = value.flatten()

    pure_value = np.zeros_like(value_flatten)
    unit = np.zeros_like(value_flatten, dtype=np.object)

    for i, item in enumerate(value_flatten):
        pure_value[i], unit[i] = bin_decompose_expr(item)

    pure_value = pure_value.reshape(shape)
    unit = unit.reshape(shape)

    if False in [unit[0] == item for item in unit]:
        raise ValueError("If the input is an array, the units for all values must be equal.")
    else:

        return pure_value.astype(np.double), unit[0]

cdef tuple bin_decompose(value):
    """
    Decompose a array with sympy expressions or a sympy expression to value and units.

    Parameters
    ----------
    value : numpy.ndarray, sympy expression
        An array with sympy expressions.

    Returns
    -------
    tuple (DTYPE_ARRAY/DTYPE_SCALAR value, object unit)
    """

    if isinstance(value, tuple(sympy.core.all_classes)):
        return bin_decompose_expr(value)
    elif isinstance(value, np.ndarray):
        return bin_decompose_expr_array(value)
    else:
        raise TypeError("{} is not a valid expression.".format(str(value)))
