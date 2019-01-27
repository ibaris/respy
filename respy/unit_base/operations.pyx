# # -*- coding: utf-8 -*-
# """
# Created on 26.01.2019 by Ismail Baris
# """
from __future__ import division
import numpy as np
cimport numpy as np
from respy.units.util import Zero, UnitError
from respy.unit_base.util cimport check_units, check_names
from cpython cimport bool
from respy.units.auxil import __NONE_UNITS__, __OPERATORS__

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


cdef DTYPE_ARRAY logical_array(DTYPE_ARRAY self, DTYPE_ARRAY other, char*operator):
    """
    Compute logical operations between two objects.
    
    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    operator : char*
        Operator name from respy.unit_base.auxil.__OPERATORS__.keys()

    Returns
    -------
    numpy.ndarray
    """
    cdef:
        object OPERATOR, other_unit
        DTYPE_ARRAY other_value

    OPERATOR = __OPERATORS__[operator]


    if hasattr(self, 'quantity'):
        pass
    else:
        raise TypeError("First argument should be a Quantity class instance.")

    if hasattr(other, 'quantity'):
        other_unit = other.unit
        other_value = other.value

    else:
        other_unit = Zero
        other_value = other

    if self.unit in __NONE_UNITS__ or other_unit in __NONE_UNITS__ or self.unit == other_unit:
        pass
    else:
        raise UnitError("Logical operators must have the same unit or one of the units must be None. ")

    return OPERATOR(self.value, other_value)

cdef tuple bitwise_array(DTYPE_ARRAY self, DTYPE_ARRAY other, char*operator, bool right_handed):
    """
    Compute bitwise operations with arrays and Quantity objects. 
    
    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    operator : char*
        Operator name from respy.unit_base.auxil.__OPERATORS__.keys()
    right_handed : bool
        If True, the order of the operation is changed:
            * not right_handed : (a, b)
            * right_handed : (b, a) 

    Returns
    -------
    tuple (DTYPE_ARRAY value, object unit, type dtype)
    """
    cdef:
        object OPERATOR, other_unit, unit
        DTYPE_ARRAY other_value, value
        bool other_constant
        np.dtype dtype

    OPERATOR = __OPERATORS__[operator]

    if hasattr(self, 'quantity'):
        pass
    else:
        raise TypeError("First argument should be a Quantity class instance.")

    if hasattr(other, 'quantity'):
        raise UnitError("Bitwise operators should not have units.")

    else:
        other_value = other
        other_unit = Zero
        other_name = b''
        other_constant = False

    if np.all(self.value % 1 == 0):
        pass
    else:
        raise TypeError("Quantity is type of {0}. This is a unsupported operand type for {1}".format(str(self.dtype),
                                                                                                     str(operator)))
    unit = self.unit

    name = self.name if not self.constant else b''
    value = OPERATOR(self.value.astype(np.int), other_value) if not right_handed else OPERATOR(other_value, self.value.astype(np.int))
    dtype = value.dtype

    return value, unit, dtype

cdef tuple operator_array(DTYPE_ARRAY self, DTYPE_ARRAY other, char*operator, bool right_handed):
    """
    Compute maths operations with arrays and Quantity objects. 
    
    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    operator : char*
        Operator name from respy.unit_base.auxil.__OPERATORS__.keys()
    right_handed : bool
        If True, the order of the operation is changed:
            * not right_handed : (a, b)
            * right_handed : (b, a) 

    Returns
    -------
    tuple (DTYPE_ARRAY value, object unit, type dtype, char* name)
    """

    cdef:
        object OPERATOR, other_unit, unit, self_unit
        DTYPE_ARRAY other_value, value
        bool other_constant
        np.dtype dtype

    if hasattr(self, 'quantity'):
        pass
    else:
        raise TypeError("First argument should be a Quantity class instance.")

    OPERATOR = __OPERATORS__[operator]

    if hasattr(other, 'quantity'):
        other_value = other.value
        other_unit = other.unit
        other_name = other.name
        other_constant = other.constant

    else:
        other_value = other
        other_unit = Zero
        other_name = b''
        other_constant = False

    name = check_names(self.name, other_name, self.constant, other_constant)
    self_unit, other_unit = check_units(self.unit, other_unit, operator)

    unit = OPERATOR(self_unit, other_unit) if not right_handed else OPERATOR(other_unit, self_unit)
    value = OPERATOR(self.value, other_value) if not right_handed else OPERATOR(other_value, self.value)
    dtype = value.dtype

    return value, unit, dtype, name


def compute_logical_operation(DTYPE_ARRAY self, DTYPE_ARRAY other, char*operator):
    """
    Compute logical operations between two objects.

    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    operator : char*
        Operator name from respy.unit_base.auxil.__OPERATORS__.keys()

    Returns
    -------
    numpy.ndarray
    """

    return logical_array(self, other, operator)


def compute_bitwise_operation(DTYPE_ARRAY self, DTYPE_ARRAY other, char*operator, bool right_handed):
    """
    Compute bitwise operations with arrays and Quantity objects.

    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    operator : char*
        Operator name from respy.unit_base.auxil.__OPERATORS__.keys()
    right_handed : bool
        If True, the order of the operation is changed:
            * not right_handed : (a, b)
            * right_handed : (b, a)

    Returns
    -------
    tuple (DTYPE_ARRAY value, object unit, type dtype)
    """

    return bitwise_array(self, other, operator, right_handed)

def compute_operation(DTYPE_ARRAY self, DTYPE_ARRAY other, char*operator, bool right_handed):
    """
    Compute maths operations with arrays and Quantity objects.

    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    operator : char*
        Operator name from respy.unit_base.auxil.__OPERATORS__.keys()
    right_handed : bool
        If True, the order of the operation is changed:
            * not right_handed : (a, b)
            * right_handed : (b, a)

    Returns
    -------
    tuple (DTYPE_ARRAY value, object unit, type dtype, char* name)
    """

    return operator_array(self, other, operator, right_handed)
