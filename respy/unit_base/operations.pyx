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
from respy.units.util import Zero, One, UnitError, DimensionError
from respy.unit_base.util cimport check_names
from cpython cimport bool
from respy.units.auxil import __NONE_UNITS__, __SAME_UNIT_OPERATOR__
import warnings
import sys

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


cdef DTYPE_ARRAY logical_array(DTYPE_ARRAY self, DTYPE_ARRAY other, object OPERATOR, bool verbose):
    """
    Compute logical operations between two objects.
    
    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    OPERATOR : object
        Operator name from respy.unit_base.auxil.__OPERATORS__.values()

    Returns
    -------
    numpy.ndarray
    """

    if hasattr(self, 'quantity'):
        pass
    else:
        raise TypeError("First argument should be a Quantity class instance.")

    if hasattr(other, 'quantity'):
        if self.unit in __NONE_UNITS__ or other.unit in __NONE_UNITS__ or self.unit == other.unit:
            pass
        else:
            if (self.dimension == other.dimension and self.dimension not in __NONE_UNITS__
                    and other.dimension not in __NONE_UNITS__):

                if verbose or other.verbose:
                    sys.stdout.write("The objects have different units, but the same dimension. Therefore \n"
                                     "the unit {0} is converted to the unit {1}.\n".format(str(other.unit), str(self.unit)))

                other = other.convert_to(self.unit)

            else:
                raise DimensionError("\nLogical operators must have the same unit or one of the units must be None. \n"
                                     "The units cannot be converted automatically because the dimension {0} is not \n"
                                     "compatible with the dimension {1}.\n".format(str(self.dimension),
                                                                                   str(other.dimension)))

        return OPERATOR(self.value, other.value)

    else:

        return OPERATOR(self.value, other)

cdef tuple bitwise_array(DTYPE_ARRAY self, DTYPE_ARRAY other, object OPERATOR, bool right_handed):
    """
    Compute bitwise operations with arrays and Quantity objects. 
    
    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    OPERATOR : object
        Operator name from respy.unit_base.auxil.__OPERATORS__.values()
    right_handed : bool
        If True, the order of the operation is changed:
            * not right_handed : (a, b)
            * right_handed : (b, a) 

    Returns
    -------
    tuple (DTYPE_ARRAY value, object unit, type dtype)
    """
    cdef:
        object other_unit, unit
        DTYPE_ARRAY other_value, value
        bool other_constant
        np.dtype dtype


    if hasattr(self, 'quantity'):
        pass
    else:
        raise TypeError("First argument should be a Quantity class instance.")

    if hasattr(other, 'quantity'):
        if other.unit in __NONE_UNITS__:
            pass
        else:
            raise UnitError("Bitwise operators should not have units.")

    else:
        other_value = other
        other_unit = Zero
        other_name = b''
        other_constant = False

    if np.all(self.value % 1 == 0):
        pass
    else:
        raise TypeError("Quantity is type of {0}. \nThis is a unsupported operand type for {1}".format(str(self.dtype),
                                                                                                     str(OPERATOR.__name__)))
    unit = self.unit

    name = self._name if not self.constant else b''
    value = OPERATOR(self.value.astype(np.int), other_value) if not right_handed else OPERATOR(other_value, self.value.astype(np.int))
    dtype = value.dtype

    return value, unit, dtype

cdef tuple operator_array(DTYPE_ARRAY self, DTYPE_ARRAY other, object OPERATOR, bool right_handed, bool verbose):
    """
    Compute maths operations with arrays and Quantity objects. 
    
    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    OPERATOR : object
        Operator name from respy.unit_base.auxil.__OPERATORS__.values()
    right_handed : bool
        If True, the order of the operation is changed:
            * not right_handed : (a, b)
            * right_handed : (b, a) 

    Returns
    -------
    tuple (DTYPE_ARRAY value, object unit, type dtype, char* name)
    """

    cdef:
        object unit
        DTYPE_ARRAY value
        np.dtype dtype

    if hasattr(self, 'quantity'):
        pass
    else:
        raise TypeError("First argument should be a Quantity class instance.")

    if hasattr(other, 'quantity'):

        if OPERATOR.__name__ in __SAME_UNIT_OPERATOR__:
            if self.unit in __NONE_UNITS__ or other.unit in __NONE_UNITS__ or self.unit == other.unit:
                unit = self.unit if self.unit not in __NONE_UNITS__ else other.unit

            else:
                if (self.dimension == other.dimension and self.dimension not in __NONE_UNITS__
                    and other.dimension not in __NONE_UNITS__):

                    if verbose or other.verbose:
                        sys.stdout.write("The objects have different units, but the same dimension. Therefore \n"
                                         "the unit {0} is converted to the unit {1}.\n".format(str(other.unit), str(self.unit)))

                    other = other.convert_to(self.unit)
                    unit = self.unit if self.unit not in __NONE_UNITS__ else other.unit

                else:
                    raise DimensionError("Logical operators must have the same unit or one of the units must be None. \n"
                                         "The units cannot be converted automatically because the dimension {0} is not \n"
                                         "compatible with the dimension {1}.\n".format(str(self.dimension),
                                                                                       str(other.dimension)))

        elif OPERATOR.__name__ == b'pow':

            if not right_handed:
                if other.unit not in __NONE_UNITS__:
                    warnings.warn("\nAn exponent should not have a unit. Thus, the unit of the \n"
                                  "exponent {0} will be ignored.\n".format(str(other.unit)))

            else:
                if self.unit not in __NONE_UNITS__:
                    warnings.warn("\nAn exponent should not have a unit. Thus, the unit of the \n"
                                  "exponent {0} will be ignored.\n".format(str(self.unit)))

            if (self.dimension == other.dimension and self.dimension not in __NONE_UNITS__
                    and other.dimension not in __NONE_UNITS__):

                if verbose or other.verbose:
                    sys.stdout.write("The objects have different units, but the same dimension. Therefore \n"
                                     "the unit {0} is converted to the unit {1}.\n".format(str(other.unit), str(self.unit)))

                other = other.convert_to(self.unit)

            unit = One if self.unit in __NONE_UNITS__ else self.unit

        elif OPERATOR.__name__ == b'mod':
            if self.unit in __NONE_UNITS__:
                unit = other.unit if other.unit is not None else One

            elif other.unit in __NONE_UNITS__:
                unit = self.unit if self.unit is not None else One

            elif self.unit == other.unit:
                unit = One

            else:
                if (self.dimension == other.dimension and self.dimension not in __NONE_UNITS__
                    and other.dimension not in __NONE_UNITS__):

                    if verbose or other.verbose:
                        sys.stdout.write("The objects have different units, but the same dimension. Therefore \n"
                                         "the unit {0} is converted to the unit {1}.\n".format(str(other.unit), str(self.unit)))

                    other = other.convert_to(self.unit)

                    unit = self.unit

                else:
                    raise DimensionError("Mod operator must have the same unit or one of the units must be None. \n"
                                         "The units cannot be converted automatically because the dimension {0} is not \n"
                                         "compatible with the dimension {1}.\n".format(str(self.dimension),
                                                                                       str(other.dimension)))

        else:
            if (self.dimension == other.dimension and self.dimension not in __NONE_UNITS__
                    and other.dimension not in __NONE_UNITS__):

                if verbose or other.verbose:
                    sys.stdout.write("The objects have different units, but the same dimension. Therefore \n"
                                     "the unit {0} is converted to the unit {1}.\n".format(str(other.unit), str(self.unit)))

                other = other.convert_to(self.unit)

            unit = OPERATOR(self.unit, other.unit) if not right_handed else OPERATOR(other.unit, self.unit)


        sname = self._name if self._name is not None else b''
        oname = other._name if other._name is not None else b''
        name = check_names(sname, oname, self.constant, other.constant)

        value = OPERATOR(self.value, other.value) if not right_handed else OPERATOR(other.value, self.value)

    else:
        if self.constant:
            name = b''
        else:
            name = self._name if self._name is not None else b''

        if OPERATOR.__name__ == b'mod':
            if self.unit in __NONE_UNITS__:
                unit = One
            else:
                unit = self.unit
        elif OPERATOR.__name__ in __SAME_UNIT_OPERATOR__:
            unit = self.unit

        else:
            unit = OPERATOR(self.unit, One) if not right_handed else OPERATOR(One, self.unit)

        value = OPERATOR(self.value, other) if not right_handed else OPERATOR(other, self.value)

    dtype = value.dtype

    return value, unit, dtype, name


def compute_logical_operation(DTYPE_ARRAY self, DTYPE_ARRAY other, object OPERATOR, bool verbose):
    """
    Compute logical operations between two objects.

    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    OPERATOR : object
        Operator name from respy.unit_base.auxil.__OPERATORS__.values()

    Returns
    -------
    numpy.ndarray
    """

    return logical_array(self, other, OPERATOR, verbose)


def compute_bitwise_operation(DTYPE_ARRAY self, DTYPE_ARRAY other, object OPERATOR, bool right_handed):
    """
    Compute bitwise operations with arrays and Quantity objects.

    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    OPERATOR : object
        Operator name from respy.unit_base.auxil.__OPERATORS__.values()
    right_handed : bool
        If True, the order of the operation is changed:
            * not right_handed : (a, b)
            * right_handed : (b, a)

    Returns
    -------
    tuple (DTYPE_ARRAY value, object unit, type dtype)
    """

    return bitwise_array(self, other, OPERATOR, right_handed)

def compute_operation(DTYPE_ARRAY self, DTYPE_ARRAY other, object OPERATOR, bool right_handed, bool verbose):
    """
    Compute maths operations with arrays and Quantity objects.

    Parameters
    ----------
    self : numpy.ndarray
        A Quantity class object.
    other : numpy.ndarray
        A numpy.ndarray.
    OPERATOR : object
        Operator name from respy.unit_base.auxil.__OPERATORS__.values()
    right_handed : bool
        If True, the order of the operation is changed:
            * not right_handed : (a, b)
            * right_handed : (b, a)

    Returns
    -------
    tuple (DTYPE_ARRAY value, object unit, type dtype, char* name)
    """

    return operator_array(self, other, OPERATOR, right_handed, verbose)
