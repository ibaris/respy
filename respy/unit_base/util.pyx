# -*- coding: utf-8 -*-
"""
Created on 27.01.2019 by Ismail Baris
"""
from __future__ import division
from respy.units.auxil import __NONE_UNITS__, __ADD_SUB__, __BITWISE__
from respy.units.util import UnitError, Zero, One
from cpython cimport bool

cdef tuple check_units(object unit1, object unit2, char*operator_name):
    """
    Check if the inputted units are compatible and make them compatible if possible.
    
    Parameters
    ----------
    unit1 : object
        First unit.
    unit2 : object
        Second unit.
    operator_name : char*
        Operator name from respy.unit_base.auxil.__OPERATORS__.keys()

    Returns
    -------
    tuple with (object, object)
    """

    if operator_name in __ADD_SUB__ or operator_name in __BITWISE__:

        if unit1 in __NONE_UNITS__ and unit2 in __NONE_UNITS__:
            unit1 = Zero
            unit2 = Zero

        elif unit1 in __NONE_UNITS__:
            unit1 = Zero if unit2 in __NONE_UNITS__ else unit2
        elif unit2 in __NONE_UNITS__:
            unit2 = Zero if unit1 in __NONE_UNITS__ else unit1

        elif unit1 == unit2:
            unit2 = Zero

            return unit1, unit2

        else:
            raise UnitError("Addition, subtraction and bitwise operations require the same unit or "
                            "one of the units must be None.")

    elif operator_name == b'pow' and unit2 not in __NONE_UNITS__:
        raise UnitError("An exponent with unit is not possible.")

    else:
        unit1 = One if unit1 in __NONE_UNITS__ else unit1
        unit2 = One if unit2 in __NONE_UNITS__ else unit2

        return unit1, unit2

cdef char*check_names(char*name1, char*name2, bool constant1, bool constant2):
    """
    Check and select the right name.
    
    Parameters
    ----------
    name1 : char*
        First name.
    name2 : char*
        Second name.
    constant1 : bool
        Choose if the first name is defined as constant. 
    constant2 : bool
        Choose if the second name is defined as constant. 

    Returns
    -------
    char*
    
    """

    if name1 == b'' and name2 == b'':
        name = b''
    elif name1 == b'' and name2 != b'':
        name = name2 if not constant1 else b''
    elif name1 != b'' and name2 == b'':
        name = name1 if not constant1 else b''
    else:
        name = b''

    return name
