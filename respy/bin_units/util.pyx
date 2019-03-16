# -*- coding: utf-8 -*-
# cython: cdivision=True
"""
Created on 15.03.2019 by Ismail Baris
"""
from __future__ import division
from respy.bin_units.conversion cimport bin_get_unit
from respy.units.auxil import One, Zero
from respy.units.dimensions import *


cdef bin_get_dimension(unit):
    cdef:
        object dimension, unit_base

    unit = bin_get_unit(unit)

    if 'Quantity' in str(type(unit)):
        try:
            dimension = unit.dimension

        except AttributeError:
            dimension = Zero

    elif 'Pow' in str(type(unit)):
        unit_base, exp = unit.args

        try:
            dimension_base = unit_base.dimension

            if dimension_base == length:

                if exp == 2:
                    dimension = area
                elif exp == 3:
                    dimension = volume
                elif exp < 0:
                    dimension = Zero
                else:
                    dimension = One

            elif exp < 0:
                dimension = Zero

            else:
                dimension = dimension_base

        except AttributeError:
            dimension = Zero

    else:
        dimension = Zero

    return dimension
