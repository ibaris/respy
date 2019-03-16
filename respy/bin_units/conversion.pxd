# -*- coding: utf-8 -*-
# cython: cdivision=True
"""
Created on 15.03.2019 by Ismail Baris
"""
import numpy as np
cimport numpy as np
from respy.bin_units.dtypes cimport DTYPE_ARRAY

cdef double[:] bin_convert_to(DTYPE_ARRAY expr, object unit)
cdef object bin_get_unit_from_str(char* unit)
cdef bin_get_unit(unit)