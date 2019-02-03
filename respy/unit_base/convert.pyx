# -*- coding: utf-8 -*-
"""
Conversion Base of Physical Quantities
--------------------------------------
Created on 24.01.2019 by Ismail Baris

This Module is the base for unit conversions of `Quantity` objects.
"""

from __future__ import division
cimport numpy as np
import numpy as np
from sympy.physics.units import convert_to as sympy_convert_to

ctypedef fused DTYPE_ARRAY:
    np.ndarray
    int[:]
    double[:]
    long long[:]
    float[:]
    int[:,:]
    double[:,:]
    long long[:,:]
    float[:,:]
    int[:,:,:]
    double[:,:,:]
    long long[:,:,:]
    float[:,:,:]


cdef double[:] convert_to(DTYPE_ARRAY expr, object unit):
    """
    Convert between units with sympy.convert to.
    
    Parameters
    ----------
    expr : numpy.ndarray
        An array with sympy unit expressions.
    unit :  sympy.core.mul.Mul, sympy.physics.units.quantities.Quantity
        The unit to which you want to convert.

    Returns
    -------
    double[:]
    
    """
    cdef:
        Py_ssize_t i, x
        double[:] value_view

    value = np.zeros_like(expr, dtype=np.double)
    value_view = value
    x = value.shape[0]

    for i in range(x):
        arg = sympy_convert_to(expr[i], unit).n()
        value_view[i] = arg.args[0]

    return value

def convert_to_unit(DTYPE_ARRAY expr, unit):
    """
    Convert between units with sympy.convert to.

    Parameters
    ----------
    expr : numpy.ndarray
        An array with sympy unit expressions.
    unit :  sympy.core.mul.Mul, sympy.physics.units.quantities.Quantity
        The unit to which you want to convert.

    Returns
    -------
    double[:]
    """
    return convert_to(expr, unit)
