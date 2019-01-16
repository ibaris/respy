from __future__ import division
cimport numpy as np
import numpy as np
from sympy.physics.units import convert_to as sympy_convert_to


cdef double[:] convert_to(np.ndarray expr, unit):
    cdef:
        Py_ssize_t i, x
        double[:] value_view

    value = np.zeros_like(expr, dtype=np.double)
    value_view = value
    x = value.shape[0]

    for i in range(x):
        arg = sympy_convert_to(expr[i], unit).n()
        value[i] = arg.args[0]

    return value

def convert_to_unit(np.ndarray expr, unit):
    return convert_to(expr, unit)
