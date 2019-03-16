# -*- coding: utf-8 -*-
# cython: cdivision=True
"""
Created on 15.03.2019 by Ismail Baris
"""
from respy.units.auxil import __NONE_UNIT_TYPES__, __NONE_DIM_TYPES__, One, Zero


cdef bin_isnone(object unit):
    if unit in __NONE_UNIT_TYPES__:
        return True
    else:
        return False

cdef bin_dimisnone(object unit):
    try:
        if unit.dimension.name in __NONE_DIM_TYPES__:
            return True
        else:
            return False

    except AttributeError:
        return True

cdef bin_dimisone(object unit):
    try:
        if unit.dimension.name == One:
            return True
        else:
            return False

    except AttributeError:
        return True

cdef bin_dimiszero(object unit):
    try:
        if unit.dimension.name == Zero:
            return True
        else:
            return False

    except AttributeError:
        return True