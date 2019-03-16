"""
Created on 15.03.2019 by Ismail Baris
"""
from __future__ import division
from respy.bin_units.conversion cimport bin_convert_to, bin_get_unit_from_str, bin_get_unit
from respy.bin_units.auxil cimport bin_isnone, bin_dimisnone, bin_dimisone, bin_dimiszero
from respy.bin_units.decomposition cimport bin_decompose
from respy.bin_units.util cimport bin_get_dimension
import numpy as np
cimport numpy as np
# from respy.bin_units.dtypes cimport DTYPE_ARRAY

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
    complex[:]
    complex[:,:]
    complex[:,:,:]

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
    return bin_convert_to(expr, unit)

def unit_isnone(object unit):
    """
    Check if a unit has a None-Typed object.

    Parameters
    ----------
    unit : object
        Unit expression.

    Returns
    -------
    bool
    """
    return bin_isnone(unit)

def dim_isnone(object unit):
    """
    Check if a dimension of a unit has a None-Typed object.

    Parameters
    ----------
    unit : object
        Unit expression.

    Returns
    -------
    bool
    """
    return bin_dimisnone(unit)

def get_unitstr(char*unit):
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
    return bin_get_unit_from_str(unit)

def decompose(value):
    """
    Decompose a array with sympy expressions or a sympy expression to value and units.

    Parameters
    ----------
    value : numpy.ndarray, sympy expression
        An array with sympy expressions.

    Returns
    -------
    tuple (DTYPE_ARRAY/DTYPE_SCALAR value, object unit)
    """

    return bin_decompose(value)

def get_unit(unit):
    """
    Get unit object from string or unit object (sympy).

    Parameters
    ----------
    unit : str, char or unit object.

    Returns
    -------
    object
    """
    return bin_get_unit(unit)

def get_dim(unit):
    """
    Get dimension from a unit object.

    Parameters
    ----------
    unit : object
        Unit expression.

    Returns
    -------
    dimension
    """

    return bin_get_dimension(unit)

def dim_isone(object unit):
    """
    Check if a dimension of a unit is One.

    Parameters
    ----------
    unit : object
        Unit expression.

    Returns
    -------
    bool
    """
    return bin_dimisone(unit)

def dim_iszero(object unit):
    """
    Check if a dimension of a unit is Zero.

    Parameters
    ----------
    unit : object
        Unit expression.

    Returns
    -------
    bool
    """
    return bin_dimiszero(unit)