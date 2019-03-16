# -*- coding: utf-8 -*-
# cython: cdivision=True
"""
Created on 15.03.2019 by Ismail Baris

Conversion Base of Physical Quantities
--------------------------------------
This Module is the base for unit conversions of `Quantity` objects.

"""
from __future__ import division
import numpy as np
cimport numpy as np

from sympy.physics.units import convert_to as sympy_convert_to
from respy.bin_units.dtypes cimport DTYPE_ARRAY
from respy.bin_units.auxil cimport bin_isnone
from respy.errors import UnitError
from respy.units.auxil import Zero, __UNITS__, __SYMPY_CLASSES__, __OPERAND__


cdef double[:] bin_convert_to(DTYPE_ARRAY expr, object unit):
    """
    Convert between units via `sympy.convert_to`.
    
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
        value_view[i] = arg.args[0] if arg.args[0] != Zero else arg

    return value

cdef object bin_get_unit_from_str(char* unit):
    """
    Get a unit object from str or char.
    
    Parameters
    ----------
    unit : char*
        Desired unit in str format. 
        
    Returns
    -------
    object
    
    """
    cdef:
        list unit_list, operand_list
        object unit_obj
        Py_ssize_t i

    unit_str = unit.split()
    unit_list = []
    operand_list = []

    for item in unit_str:
        if item in __OPERAND__:
            operand_list.append(item)

        else:
            try:
                item = int(item)
                unit_list.append(item)

            except ValueError:
                try:
                    unit_list.append(__UNITS__[item])

                except KeyError:
                    raise UnitError("{} is not a valid unit. There should be spaces between the characters.".format(str(item)))

    unit_obj = unit_list[0]

    for i in range(1, len(unit_list)):
        item = unit_list[i]
        try:
            if operand_list[i - 1] == b'*':
                unit_obj *= item
            elif operand_list[i - 1] == b'/':
                unit_obj /= item
            elif operand_list[i - 1] == b'+':
                unit_obj += item
            elif operand_list[i - 1] == b'-':
                unit_obj -= item
            elif operand_list[i - 1] == b'**':
                unit_obj **= item
        except IndexError:
            pass

    return unit_obj

cdef bin_get_unit(unit):
    """
    Get unit object from string or unit object (sympy).

    Parameters
    ----------
    unit : str, char or unit object.

    Returns
    -------
    object
    """
    if isinstance(unit, __SYMPY_CLASSES__) or bin_isnone(unit):
        return unit
    elif isinstance(unit, str):
        return bin_get_unit_from_str(unit)
    else:
        raise UnitError("{} is not a valid unit.".format(str(unit)))
