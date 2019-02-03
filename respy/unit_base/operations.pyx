# -*- coding: utf-8 -*-
"""
Operation Base of Physical Quantities
-------------------------------------
Created on 26.01.2019 by Ismail Baris

This Module is the base for every operation of `Quantity` objects.

"""
from __future__ import division
import numpy as np
cimport numpy as np
from respy.units.util import Zero, One, UnitError
from respy.unit_base.util cimport check_names
from cpython cimport bool
from respy.units.auxil import __NONE_UNITS__, __OPERATORS__, __ADD_SUB__, __BITWISE__
import warnings

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

    name = self._name if not self.constant else b''
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
        other_name = other._name
        other_constant = other.constant

    else:
        other_value = other
        other_unit = One
        other_name = b''
        other_constant = False

    name = check_names(self._name, other_name, self.constant, other_constant)

    if operator in __ADD_SUB__ or operator in __BITWISE__:
        if self.unit in __NONE_UNITS__:
            unit = other_unit if other_unit not in __NONE_UNITS__ else One

        elif other_unit in __NONE_UNITS__:
            unit = self.unit

        elif other_unit == self.unit:
            unit = self.unit

        else:
            raise UnitError("Addition, subtraction and bitwise operations require the same unit or "
                            "one of the units must be None.")

    elif operator == b'**':
        if other_unit not in __NONE_UNITS__:
            warnings.warn("An exponent should not have a unit. Thus, the unit of the "
                          "exponent {0} will be ignored.".format(str(other_unit)))

            unit = One if self.unit in __NONE_UNITS__ else self.unit

        else:
            unit = One if self.unit in __NONE_UNITS__ else self.unit

    else:
        unit = OPERATOR(self.unit, other_unit) if not right_handed else OPERATOR(other_unit, self.unit)

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
