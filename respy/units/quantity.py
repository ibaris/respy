# -*- coding: utf-8 -*-
"""
Physical Quantities
-------------------
Created on 10.01.2019 by Ismail Baris

This module defines the `Quantity` objects. A Quantity object represents a number with some an associated unit.
`Quantity` objects are subclasses of numpy.ndarray. Thus, a `Quantity` object support operations like ordinary arrays,
but will deal with unit conversions internally. The base of the `Quantity` object is programmed in `Cython`.
"""
from __future__ import division

import inspect

import numpy as np
from respy.unit_base.auxil import decompose_expr_to_atoms
from respy.unit_base.auxil import get_unit, get_dimension
from respy.unit_base.convert import convert_to_unit
from respy.unit_base.operations import compute_logical_operation, compute_bitwise_operation, compute_operation

import util as util
from respy.units.auxil import __NONE_UNITS__, __OPERATOR__
from respy.units.util import Zero, One, UnitError
from respy.units.unit_ufuncs import (__CONVERT__MATH__, __MATH_UNIT_GETS_LOST__, __MATH_UNIT_REMAINS_STABLE__,
                                     __CHECK_UNIT__, __MATH_LOGICAL_AND_MORE__, __NOT_IMPLEMENTED__)

np.seterr(divide='ignore', invalid='ignore')


class Quantity(np.ndarray):
    """ Physical Quantities

    This module defines the `Quantity` objects. A Quantity object represents a number with some an associated unit.

    Attributes
    ----------
    Quantity.value : np.ndarray
        The numerical value of this quantity in the units given by unit.
    Quantity.unit : sympy.physics.units.quantities.Quantity
        An object that represents the unit associated with the input value.
    Quantity.dtype : type
        The data type of the value
    Quantity.copy: bool
        The entered copy bool value.
    Quantity.order : str
        Order of the array.
    Quantity.subok : bool
        The entered subok value.
    Quantity.ndmin : int
        Minimum number of dimensions
    Quantity.name : str
        Name of the Quantity
    Quantity.constant : bool
        Information about if the Quantity is an constant or not.
    Quantity.unitstr : str
        Parameter unit as str.
    Quantity.unit_mathstr : str
        Parameter unit as math text.
    Quantity.label : str
        Parameter name and unit as math text.
    Quantity.expr : np.ndarray
        The whole expression (value * unit) as sympy.core.mul.Mul.
    Quantity.tolist : list
        Value and unit as a list.

    Methods
    -------
    decompose()
        Return value as np.ndarray and unit as sympy.physics.units.quantities.Quantity object.
    decompose_expr(expr)
        Extract value and unit from a sympy.core.mul.Mul object.
    set_name(name)
        Set a name for the current Quantity.
    convert_to(unit, inplace=True)
        Convert unit to another units.
    set_constant(bool)
        Set a `Quantity` object as constant. In this case, every operation will drop the name of the Quantity.
    Raises
    ------
    UnitError
    DimensionError

    See Also
    --------
    respry.units.util.Units

    """

    def __new__(cls, value, unit=None, dtype=None, copy=True, order=None,
                subok=False, ndmin=0, name=None, constant=True, verbose=False):
        """
        The Quantity object is meant to represent a value that has some unit associated with the number.

        Parameters
        ----------
        value : float, int, numpy.ndarray, sympy.core.all_classes
            The numerical value of this quantity in the units given by unit.

        unit : sympy.physics.units.quantities.Quantity, str
            An object that represents the unit associated with the input value.
            Must be an `sympy.physics.units.quantities.Quantity` object or a string parsable by
            the :mod:`~respy.units` package.

        dtype : numpy.dtype, type, int, float, double, optional
            The dtype of the resulting Numpy array or scalar that will
            hold the value.  If not provided, it is determined from the input,
            except that any input that cannot represent float (integer and bool)
            is converted to float.

        copy : bool, optional
            If `True` (default), then the value is copied.  Otherwise, a copy will
            only be made if ``__array__`` returns a copy, if value is a nested
            sequence, or if a copy is needed to satisfy an explicitly given
            ``dtype``.  (The `False` option is intended mostly for internal use,
            to speed up initialization where a copy is known to have been made.
            Use with care.)

        order : {'C', 'F', 'A'}, optional
            Specify the order of the array.  As in `~numpy.array`.  This parameter
            is ignored if the input is a `Quantity` and ``copy=False``.

        subok : bool, optional
            If `False` (default), the returned array will be forced to be a
            `Quantity`.

        ndmin : int, optional
            Specifies the minimum number of dimensions that the resulting array
            should have.  Ones will be pre-pended to the shape as needed to meet
            this requirement.  This parameter is ignored if the input is a
            `Quantity` and ``copy=False``.
        name : str
            A name for the created Quantity.
        constant : bool
            If True and the constant has a name the name will be replaced after a operation.

        """

        x = np.array(value, dtype=dtype, copy=copy, order=order, subok=subok, ndmin=ndmin)
        x = np.atleast_1d(x)

        if x.dtype == int:
            dtype = np.double
            x = x.astype(dtype)
        else:
            pass

        obj = x.view(type=cls)

        if unit is None:
            obj._unit = Zero
        else:
            obj._unit = get_unit(unit)

        obj._dimension = get_dimension(obj._unit)

        obj.value = x
        obj._dtype = x.dtype

        if name is None:
            obj._name = b''
        else:
            obj._name = name

        obj.constant = constant

        obj.copy = copy
        obj.order = order
        obj.subok = subok
        obj.ndmin = ndmin
        obj.quantity = True
        obj.verbose = verbose

        return obj

    # --------------------------------------------------------------------------------------------------------
    # Magic Methods
    # --------------------------------------------------------------------------------------------------------
    def __repr__(self):
        prefix = '<{0} '.format(self.__class__.__name__)
        sep = ', '
        arrstr = np.array2string(self,
                                 separator=sep,
                                 prefix=prefix)

        if self._name is None or self._name is b'':
            return '{0}{1} [{2}]>'.format(prefix, arrstr, self.unitstr)

        else:
            return '{0}{1} {2} in [{3}]>'.format(prefix, arrstr, self.name, self.unitstr)

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        else:
            self._unit = getattr(obj, '_unit', None)
            self.value = getattr(obj, 'value', None)
            self._name = getattr(obj, 'name', None)
            self.constant = getattr(obj, 'constant', None)
            self._dtype = getattr(obj, '_dtype', None)
            self.copy = getattr(obj, 'copy', None)
            self.order = getattr(obj, 'order', None)
            self.subok = getattr(obj, 'subok', None)
            self.ndmin = getattr(obj, 'ndmin', None)
            self._dimension = getattr(obj, '_dimension', None)
            self.quantity = getattr(obj, 'quantity', None)
            self.verbose = getattr(obj, 'verbose', None)

    def __array_wrap__(self, out_arr, context=None):
        return np.ndarray.__array_wrap__(self, out_arr, context)
        # return self.__create_new_instance(self.value)

    def __array_ufunc__(self, function, method, *inputs, **kwargs):
        if (function.__name__ not in __MATH_UNIT_REMAINS_STABLE__
                and function.__name__ not in __MATH_UNIT_GETS_LOST__
                and function.__name__ not in __CONVERT__MATH__
                and function.__name__ not in __CHECK_UNIT__
                and function.__name__ not in __MATH_LOGICAL_AND_MORE__):
            raise NotImplementedError

        try:
            nin = function.nin
        except AttributeError:
            if function.__name__ in __MATH_UNIT_REMAINS_STABLE__:
                unit = self.unit
            else:
                unit = One

            value = (self.value,)
            result = super(Quantity, self).__array_ufunc__(function, method, *value, **kwargs)

            dtype = result.dtype

            return self.__create_new_instance(result[0] if len(result) == 1 else result,
                                              unit,
                                              self._name if not self.constant else b'',
                                              dtype)

        if function.nin == 1:
            value = (self.value,)
            unit = (self.unit,)
            result = super(Quantity, self).__array_ufunc__(function, method, *value, **kwargs)

            if function.__name__ in __MATH_UNIT_GETS_LOST__:
                unit = One
            elif function.__name__ in __MATH_UNIT_REMAINS_STABLE__:
                unit = self.unit
            elif function.__name__ in __CONVERT__MATH__.keys():
                try:
                    unit_ufunc = __CONVERT__MATH__[function.__name__]
                    unit = unit_ufunc(self.unit)
                    unit = unit.n()

                except (AttributeError, TypeError):
                    unit = One

            elif function.__name__ in __MATH_LOGICAL_AND_MORE__:
                return result

            else:
                try:
                    unit = super(Quantity, self).__array_ufunc__(function, method, *unit, **kwargs)

                except (AttributeError, TypeError):
                    unit = One

            if function.nout == 2:
                dtype1 = result[0].dtype
                dtype2 = result[1].dtype

                dtype = (dtype1, dtype2)

                for i in range(2):
                    return self.__create_new_instance(result[i][0] if len(result[i]) == 1 else result[i],
                                                      unit,
                                                      self._name if not self.constant else b'',
                                                      dtype[i])

            else:
                dtype = result.dtype

                return self.__create_new_instance(result[0] if len(result) == 1 else result,
                                                  unit,
                                                  self._name if not self.constant else b'',
                                                  dtype)

        elif function.nin == 2:
            values = self.__check_values(*inputs)
            units = list()

            for item in inputs:
                units.append(item.unit if hasattr(item, 'quantity') else One)

            units = tuple(units)

            if function.__name__ in __CHECK_UNIT__:
                if units[1] == One or units[0] == units[1]:
                    try:
                        unit = super(Quantity, self).__array_ufunc__(function, method, *units, **kwargs)

                    except (AttributeError, TypeError):
                        unit = One
                else:
                    raise UnitError("Units are not the same")

            elif function.__name__ in __MATH_UNIT_GETS_LOST__:
                unit = One
            elif function.__name__ in __MATH_UNIT_REMAINS_STABLE__:
                unit = units[0] if units[0] != One else units[1]
            elif function.__name__ in __MATH_LOGICAL_AND_MORE__:
                return super(Quantity, self).__array_ufunc__(function, method, *values, **kwargs)

            else:
                try:
                    unit = super(Quantity, self).__array_ufunc__(function, method, *units, **kwargs)

                except (AttributeError, TypeError):
                    unit = One

            result = super(Quantity, self).__array_ufunc__(function, method, *values, **kwargs)

            if function.nout == 2:
                dtype1 = result[0].dtype
                dtype2 = result[1].dtype

                dtype = (dtype1, dtype2)

                nout = list()
                for i in range(2):
                    nout.append(self.__create_new_instance(result[i][0] if len(result) == 1 else result[i],
                                                           unit,
                                                           self._name if not self.constant else b'',
                                                           dtype[i]))

                return tuple(nout)

            else:
                dtype = result.dtype

                return self.__create_new_instance(result[0] if len(result) == 1 else result,
                                                  unit,
                                                  self._name if not self.constant else b'',
                                                  dtype)

        else:
            raise NotImplementedError

    # --------------------------------------------------------------------------------------------------------
    # Operator
    # --------------------------------------------------------------------------------------------------------
    # Attribute Operations -------------------------------------------------------------------------------
    def __getitem__(self, item):
        value = super(Quantity, self).__getitem__(item)

        return self.__create_new_instance(value, self.unit, self._name)

    # Mathematical Operations ----------------------------------------------------------------------------
    # Left Operations -------------------------------------------------------------------------------
    def __mul__(self, other):

        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=False, verbose=self.verbose)

        if unit is None:
            unit = Zero

        return self.__create_new_instance(value, unit, name, dtype)

    def __truediv__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=False, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    def __floordiv__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=False, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    def __mod__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=False, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    __div__ = __truediv__

    def __add__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=False, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    def __sub__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=False, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    def __pow__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=False, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    def __lshift__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        return compute_bitwise_operation(self, other, operator, right_handed=False)

    def __rshift__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        return compute_bitwise_operation(self, other, operator, right_handed=False)

    def __and__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        return compute_bitwise_operation(self, other, operator, right_handed=False)

    def __or__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        return compute_bitwise_operation(self, other, operator, right_handed=False)

    def __xor__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        return compute_bitwise_operation(self, other, operator, right_handed=False)

    # Right Operations --------------------------------------------------------------------------------
    __rmul__ = __mul__
    __radd__ = __add__

    def __rtruediv__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=True, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    __rdiv__ = __rtruediv__

    def __rsub__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=True, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    def __rlshift__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        return compute_bitwise_operation(self, other, operator, right_handed=True)

    def __rrshift__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        return compute_bitwise_operation(self, other, operator, right_handed=True)

    def __rfloordiv__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=True, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    def __rmod__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=True, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    def __rpow__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value, unit, dtype, name = compute_operation(self, other, operator, right_handed=True, verbose=self.verbose)

        return self.__create_new_instance(value, unit, name, dtype)

    def __rand__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        return compute_bitwise_operation(self, other, operator, right_handed=True)

    def __ror__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        return compute_bitwise_operation(self, other, operator, right_handed=True)

    def __rxor__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]

        return compute_bitwise_operation(self, other, operator, right_handed=True)

    # Augmented Assignment -------------------------------------------------------------------------------
    __iadd__ = __add__
    __isub__ = __sub__
    __imul__ = __mul__
    __ifloordiv__ = __floordiv__
    __idiv__ = __div__
    __itruediv__ = __truediv__
    __imod__ = __mod__
    __ipow__ = __pow__
    __ilshift__ = __lshift__
    __irshift__ = __rshift__
    __iand__ = __and__
    __ior__ = __or__
    __ixor__ = __xor__

    # --------------------------------------------------------------------------------------------------------
    #  Comparison
    # --------------------------------------------------------------------------------------------------------
    def __eq__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]
        return compute_logical_operation(self, other, operator, self.verbose)

    def __ne__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]
        return compute_logical_operation(self, other, operator, self.verbose)

    def __lt__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]
        return compute_logical_operation(self, other, operator, self.verbose)

    def __gt__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]
        return compute_logical_operation(self, other, operator, self.verbose)

    def __le__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]
        return compute_logical_operation(self, other, operator, self.verbose)

    def __ge__(self, other):
        other = self.__check_other(other)
        operator = __OPERATOR__[inspect.currentframe().f_code.co_name]
        return compute_logical_operation(self, other, operator, self.verbose)

    # --------------------------------------------------------------------------------------------------------
    # Numeric Magic Methods
    # --------------------------------------------------------------------------------------------------------
    def __pos__(self):
        OPERATOR = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value = OPERATOR(self.value)
        return self.__create_new_instance(value, self.unit, self._name)

    def __neg__(self):
        OPERATOR = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value = OPERATOR(self.value)
        return self.__create_new_instance(value, self.unit, self._name)

    def __abs__(self):
        OPERATOR = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value = OPERATOR(self.value)
        return self.__create_new_instance(value, self.unit, self._name)

    def __invert__(self):
        OPERATOR = __OPERATOR__[inspect.currentframe().f_code.co_name]

        value = OPERATOR(self.value)
        return self.__create_new_instance(value, self.unit, self._name)

    def __iter__(self):
        def iter_over_value(unit, name):
            for item in self.value:
                yield self.__create_new_instance(item, unit, name)

        return iter_over_value(self.unit, self._name)

    # --------------------------------------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------------------------------------
    @property
    def real(self):
        return self.__create_new_instance(self.value.real, unit=self.unit, name=self._name, dtype=self.value.real.dtype)

    @property
    def imag(self):
        return self.__create_new_instance(self.value.imag, unit=self.unit, name=self._name, dtype=self.value.imag.dtype)

    @property
    def dimension(self):
        if self._dimension in __NONE_UNITS__:
            return Zero
        else:
            return self._dimension

    @property
    def name(self):
        if self._name == b'' or self._name is None:
            return None
        else:
            return self._name

    @property
    def unit(self):
        if self._unit in __NONE_UNITS__:
            return Zero
        else:
            return self._unit.n()

    @property
    def unitstr(self):
        """
        Return the unit of the expression as string.

        Returns
        -------
        unit : str
        """

        if self.unit in __NONE_UNITS__:
            return '-'
        else:
            return str(self.unit)

    @property
    def unit_mathstr(self):
        """
        Return the unit of the expression as math text of form r'$unit$'.

        Returns
        -------
        unit : str
        """

        if self.unit in __NONE_UNITS__:
            return '-'
        else:
            unit = r'$' + self.unitstr.replace('**', '^') + '$'

            return unit

    @property
    def label(self):
        """
        Return the name and the unit of the Quantity as math text.

        Returns
        -------
        label : str
        """

        return self.name + ' ' + '\n' + ' in ' + '[' + self.unit_mathstr + ']'

    @property
    def expr(self):
        """
        Return the expression.

        Returns
        -------
        expr : numpy.ndarray with sympy.core.mul.Mul
        """
        return self.value * self.unit

    @property
    def tolist(self):
        """
        Convert values and units to list.

        Returns
        -------
        tuple with two lists ([values], [units])
        """
        return self.value.tolist(), [self.unit]

    # --------------------------------------------------------------------------------------------------------
    # Callable Methods
    # --------------------------------------------------------------------------------------------------------
    def create_arraystr(self, prefix=None, name=None):
        """
        Create a new array string for repr purpose.

        Parameters
        ----------
        prefix : str or None
            If None the prefix '<Quantity' will be used.
        name : str or None
            Name of the Quantity.

        Returns
        -------
        str
        """
        arrstr = np.array2string(self,
                                 separator=', ',
                                 prefix=prefix)

        if prefix is None:
            prefix = '<{0} '.format(self.__class__.__name__)
        else:
            prefix = '<{0} '.format(prefix)

        if name is None:
            if self.name is None or self.name is b'':
                return '{0}{1} [{2}]>'.format(prefix, arrstr, self.unitstr)
            else:
                return '{0}{1} {2} in [{3}]>'.format(prefix, arrstr, self.name, self.unitstr)
        else:
            return '{0}{1} {2} in [{3}]>'.format(prefix, arrstr, name, self.unitstr)

    def set_constant(self, constant):
        if isinstance(constant, bool):
            self.constant = constant
        else:
            raise ValueError("Constant must be True or False")

    def decompose(self):
        """
        Decompose values and units.

        Returns
        -------
        tuple with values and units.
        """
        return self.value, self.unit

    @staticmethod
    def decompose_expr(expr, quantity=True):
        """
        Extract value and unit from an sympy expression or an array with sympy expressions.

        Parameters
        ----------
        expr :numpy.ndarray, sympy.core.mul.Mul
            Sympy expression
        quantity : bool
            If True (default), the output is an Quantity object.

        Returns
        -------
        tuple with (values, units)
        """
        if quantity:
            value, unit = decompose_expr_to_atoms(expr)
            return Quantity(value, unit)
        else:
            return decompose_expr_to_atoms(expr)

    def set_name(self, name):
        """
        Set name of Quantity.

        Parameters
        ----------
        name : str
            Name of Quantity.

        Returns
        -------
        None
        """
        self._name = name

    def convert_to(self, unit):
        """
        Convert a quantity to another unit.

        Parameters
        ----------
        unit : sympy.physics.units.quantities.Quantity, str
            An object that represents the unit associated with the input value.
            Must be an `sympy.physics.units.quantities.Quantity` object or a string parsable by
            the :mod:`~respy.units` package.

        Returns
        -------
        respy.units.Quantity or None

        """
        unit = get_unit(unit)

        if unit == 1 / util.Units.time.s and self.dimension == util.dimensions.frequency:
            scaled_value = self.value.astype(self._dtype) * self.unit.scale_factor

            value = scaled_value / util.Units[str(self.dimension.name)]['Hz'].scale_factor

        elif hasattr(unit, 'dimension'):

            if self.unit == 1 / util.Units.time.s and unit.dimension == util.dimensions.frequency:
                scaled_value = self.value.astype(self._dtype)

                value = scaled_value / util.Units[str(unit.dimension.name)][str(unit)].scale_factor

            elif unit.dimension == self.dimension:
                scaled_value = self.value.astype(self._dtype) * util.Units[str(unit.dimension.name)][
                    str(self.unit)].scale_factor

                value = scaled_value / util.Units[str(unit.dimension.name)][str(unit)].scale_factor

            else:
                value = np.zeros_like(self.value, dtype=self._dtype)

                if len(self.value) == 1:
                    arg = convert_to_unit(self.expr, unit)
                    value[0] = arg.base
                    value = value.flatten()

                else:
                    shape = self.value.shape
                    expr = self.expr.flatten()
                    value = convert_to_unit(expr, unit)

                    value = value.base
                    value = value.reshape(shape)

        else:
            value = np.zeros_like(self.value, dtype=self._dtype)

            if len(self.value) == 1:
                arg = convert_to_unit(self.expr, unit)
                value[0] = arg.base
                value = value.flatten()

            else:
                shape = self.value.shape
                expr = self.expr.flatten()
                value = convert_to_unit(expr, unit)

                value = value.base
                value = value.reshape(shape)

        dtype = self._dtype

        return self.__create_new_instance(value, unit, self._name)

    # --------------------------------------------------------------------------------------------------------
    # Private Methods
    # --------------------------------------------------------------------------------------------------------

    def __set_attributes(self, unit, value, dtype, copy, order, subok, constant, ndmin, name):

        self.value = value
        self._dtype = dtype
        self.copy = copy
        self.order = order
        self.subok = subok
        self.constant = constant
        self.ndmin = ndmin
        self._name = name

        self._unit = get_unit(unit)
        self._dimension = get_dimension(self._unit)

    def __create_new_instance(self, value, unit=None, name=None, dtype=None):

        quantity_subclass = self.__class__

        unit = get_unit(unit)

        if dtype is None:
            dtype = self._dtype
        else:
            pass

        value = np.array(value, dtype=dtype, copy=False, order=self.order,
                         subok=self.subok)

        value = np.atleast_1d(value)
        view = value.view(quantity_subclass)

        view.__set_attributes(unit, value, dtype, self.copy, self.order, self.subok, self.constant, self.ndmin, name)
        view.__array_finalize__(view)

        return view

    def __check_other(self, other):
        if hasattr(other, 'quantity'):
            pass
        else:
            other = np.atleast_1d(np.asarray(other))

        return other

    def __check_values(self, *values):
        results = list()

        for val in values:
            results.append(val.value if hasattr(val, 'quantity') else np.atleast_1d(np.asarray(val)))

        return results
