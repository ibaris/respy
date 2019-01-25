from __future__ import division

import inspect
import operator

import numpy as np
import sympy

import respy
import util as util
from respy.base import unit_base
from respy.units.util import One, UnitError

__OPERATORS__ = {'+': operator.add,
                 '/': operator.truediv,
                 '//': operator.floordiv,
                 '&': operator.and_,
                 '^': operator.xor,
                 '~': operator.invert,
                 '|': operator.or_,
                 '**': operator.pow,
                 '<<': operator.lshift,
                 '*': operator.mul,
                 '>>': operator.rshift,
                 '-': operator.sub,
                 '<': operator.lt,
                 '<=': operator.le,
                 '==': operator.eq,
                 '!=': operator.ne,
                 '>=': operator.ge,
                 '>': operator.gt,
                 '%': operator.mod,
                 'abs': operator.abs,
                 'pos': operator.pos,
                 'neg': operator.neg}

__UFUNC_NAME__ = {'__add__': '+',
                  '__truediv__': '/',
                  '__rtruediv__': '/',
                  '__floordiv__': '//',
                  '__rfloordiv__': '//',
                  '__and__': '&',
                  '__rand__': '&',
                  '__xor__': '^',
                  '__rxor__': '^',
                  '__or__': '|',
                  '__ror__': '|',
                  '__pow__': '**',
                  '__rpow__': '**',
                  '__lshift__': '<<',
                  '__rlshift__': '<<',
                  '__mul__': '*',
                  '__rshift__': '>>',
                  '__rrshift__': '>>',
                  '__sub__': '-',
                  '__rsub__': '-',
                  '__lt__': '<',
                  '__le__': '<=',
                  '__eq__': '==',
                  '__ne__': '!=',
                  '__ge__': '>=',
                  '__gt__': '>',
                  '__mod__': '%',
                  '__rmod__': '%',
                  '__abs__': 'abs',
                  '__pos__': 'pos',
                  '__neg__': 'neg',
                  '__invert__': '~'}


class Quantity(np.ndarray):
    def __new__(cls, value, unit=None, dtype=None, copy=True, order=None,
                subok=False, ndmin=0, name=None, constant=False):
        """
        The Quantity object is meant to represent a value that has some unit associated with the number.

        Parameters
        ----------
        value : float, int, numpy.ndarray, str, sympy.core.mul.Mul, sympy.physics.units.quantities.Quantity
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

        Attributes
        ----------
        value : np.ndarray
            The numerical value of this quantity in the units given by unit.
        unit : sympy.physics.units.quantities.Quantity
            An object that represents the unit associated with the input value.
        dtype : type
            The data type of the value
        copy: bool
            The entered copy bool value.
        order : str
            Order of the array.
        subok : bool
            The entered subok value.
        ndmin : int
            Minimum number of dimensions
        name : str
            Name of the Quantity
        constant : bool
            Information about if the Quantity is an constant or not.
        unitstr : str
            Parameter unit as str.
        math_text : str
            Parameter unit as math text.
        label : str
            Parameter name and unit as math text.
        expr : np.ndarray
            The whole expression (value * unit) as sympy.core.mul.Mul.
        tolist : list
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

        Raises
        ------
        UnitError
        DimensionError

        See Also
        --------
        respry.units.util.Units

        """

        if isinstance(value, tuple(sympy.core.all_classes)):
            copy_value = value
            value = copy_value.args[0]
            value = float(value)

            if len(copy_value.args[1:]) > 1:
                unit = copy_value.args[1]

                for item in copy_value.args[2:]:
                    unit *= item
            else:
                unit = copy_value.args[1]

        x = np.array(value, dtype=dtype, copy=copy, order=order, subok=subok, ndmin=ndmin)
        x = np.atleast_1d(x)

        if x.dtype == int:
            dtype = np.double
            x = x.astype(dtype)
        else:
            pass

        obj = x.view(type=cls)

        if unit is None:
            obj.unit = None
            obj.dimension = None
        else:
            obj.unit = util.def_unit(unit)
            try:
                obj.dimension = obj.unit.dimension.name

                if obj.dimension == 1:
                    obj.dimension = None

            except AttributeError:
                obj.dimension = None

        obj.value = x
        obj._dtype = x.dtype
        obj.name = name
        obj.constant = constant

        obj.copy = copy
        obj.order = order
        obj.subok = subok
        obj.ndmin = ndmin
        obj.quantity = True

        return obj

    # --------------------------------------------------------------------------------------------------------
    # Magic Methods
    # --------------------------------------------------------------------------------------------------------
    def __repr__(self):
        if self.name is None:
            prefix = '<{0} '.format(self.__class__.__name__)
            sep = ', '
            arrstr = np.array2string(self,
                                     separator=sep,
                                     prefix=prefix)

            return '{0}{1} [{2}]>'.format(prefix, arrstr, self.unitstr)

        else:
            prefix = '<{0} '.format(self.__class__.__name__)
            sep = ', '
            arrstr = np.array2string(self,
                                     separator=sep,
                                     prefix=prefix)

            return '{0}{1} {2} in [{3}]>'.format(prefix, arrstr, self.name, self.unitstr)

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        else:
            self.unit = getattr(obj, 'unit', None)
            self.value = getattr(obj, 'value', None)
            self.name = getattr(obj, 'name', None)
            self.constant = getattr(obj, 'constant', None)
            self._dtype = getattr(obj, '_dtype', None)
            self.copy = getattr(obj, 'copy', None)
            self.order = getattr(obj, 'order', None)
            self.subok = getattr(obj, 'subok', None)
            self.ndmin = getattr(obj, 'ndmin', None)
            self.dimension = getattr(obj, 'dimension', None)
            self.quantity = getattr(obj, 'quantity', None)

    def __array_wrap__(self, out_arr, context=None):
        return np.ndarray.__array_wrap__(self, out_arr, context)

    # --------------------------------------------------------------------------------------------------------
    # Operator
    # --------------------------------------------------------------------------------------------------------
    # Attribute Operations -------------------------------------------------------------------------------
    def __getitem__(self, item):
        value = self.value[item]
        return self.__create_new_instance(value, self.unit, self.name)

    # Mathematical Operations ----------------------------------------------------------------------------
    # Left Operations -------------------------------------------------------------------------------
    def __sympy_array(self, value):
        shape = value.shape
        value_flatten = value.flatten()

        value = np.zeros_like(value_flatten)
        unit = np.zeros_like(value_flatten, dtype=np.object)

        for i, item in enumerate(value_flatten):
            value[i], unit[i] = Quantity.decompose_expr(item)

        value = value.reshape(shape)
        unit = unit.reshape(shape)

        if np.any(unit[0] == unit):
            value = value.astype(np.double)

            return value, unit[0]
        else:
            raise ValueError("If the input is an array with values the units must for all values equal.")

    def __DO_COMPARISON(self, other, OPERATOR, rhanded=False):
        if isinstance(other, (self.__class__, type(respy.units.quantity.Quantity), np.ndarray)):

            if hasattr(other, 'quantity'):
                other_unit = other.unit
                other_value = other.value

                if self.unit != other_unit:
                    raise UnitError("Logical or shift operators require the same unit.")

                else:
                    pass

                value = OPERATOR(self.value, other_value)

            elif other.dtype == np.object:
                try:
                    other_value, other_unit = self.__sympy_array(other)

                    if self.unit != other_unit:
                        raise UnitError("Logical or shift operators require the same unit.")

                    else:
                        pass

                    value = OPERATOR(self.value, other_value)

                except AttributeError:
                    raise TypeError("Data type of {0} not understood.".format(str(other)))
            else:
                pass

        elif isinstance(other, tuple(sympy.core.all_classes)):
            other_value, other_unit = Quantity.decompose_expr(other)

            if self.unit != other_unit:
                raise UnitError("Logical or shift operators require the same unit.")

            else:
                pass

            value = OPERATOR(self.value, other_value)

        else:
            value = OPERATOR(self.value, other)

        return value

    def __DO_LOGICAL(self, other, OPERATOR, rhanded=False):
        if isinstance(other, (self.__class__, type(respy.units.quantity.Quantity), np.ndarray)):

            if hasattr(other, 'quantity'):
                other_unit = other.unit
                other_value = other.value

                if self.unit != other_unit:
                    raise UnitError("Logical or shift operators require the same unit.")

                else:
                    unit = self.unit

                value = OPERATOR(self.value, other_value) if not rhanded else OPERATOR(other_value, self.value)
                name = self.__get_name(other)

            elif other.dtype == np.object:
                try:
                    other_value, other_unit = self.__sympy_array(other)

                    if self.unit != other_unit:
                        raise UnitError("Logical or shift operators require the same unit.")

                    else:
                        unit = self.unit

                    value = OPERATOR(self.value, other_value) if not rhanded else OPERATOR(other_value, self.value)
                    name = None

                except AttributeError:
                    raise TypeError("Data type of {0} not understood.".format(str(other)))
            else:
                value = OPERATOR(self.value, other) if not rhanded else OPERATOR(other, self.value)
                unit = self.unit
                name = self.name if not self.constant else None

        elif isinstance(other, tuple(sympy.core.all_classes)):
            other_value, other_unit = Quantity.decompose_expr(other)

            if self.unit != other_unit:
                raise UnitError("Logical or shift operators require the same unit.")

            else:
                unit = self.unit

            value = OPERATOR(self.value, other_value) if not rhanded else OPERATOR(other_value, self.value)
            name = self.name if not self.constant else None

        else:
            value = OPERATOR(self.value, other) if not rhanded else OPERATOR(other, self.value)
            unit = self.unit
            name = self.name if not self.constant else None

        dtype = value.dtype
        return self.__create_new_instance(value, unit, name, dtype)

    def __DO_OPERATOR(self, other, OPERATOR, rhanded=False):
        name = OPERATOR.__name__

        if isinstance(other, (self.__class__, type(respy.units.quantity.Quantity), np.ndarray)):

            if hasattr(other, 'quantity'):
                other_unit = other.unit
                other_value = other.value

                if name == 'add' or name == 'sub':
                    if self.unit != other_unit:
                        raise UnitError("Addition and subtraction require the same unit.")
                    else:
                        unit = self.unit

                else:
                    unit = OPERATOR(self.unit, other_unit) if not rhanded else OPERATOR(other_unit, self.unit)

                if name == 'pow':
                    raise UnitError("An exponent with one unit is not possible.")

                value = OPERATOR(self.value, other_value) if not rhanded else OPERATOR(other_value, self.value)
                name = self.__get_name(other)

            elif other.dtype == np.object:
                try:
                    other_value, other_unit = self.__sympy_array(other)
                    if name == 'add' or name == 'sub':
                        if self.unit != other_value:
                            raise UnitError("Addition and subtraction require the same unit.")
                        else:
                            unit = self.unit

                    else:
                        unit = OPERATOR(self.unit, other_unit) if not rhanded else OPERATOR(other_unit, self.unit)

                    if name == 'pow':
                        raise UnitError("An exponent with one unit is not possible.")

                    value = OPERATOR(self.value, other_value) if not rhanded else OPERATOR(other_value, self.value)
                    name = None

                except AttributeError:
                    raise TypeError("Data type of {0} not understood.".format(str(other)))
            else:
                value = OPERATOR(self.value, other) if not rhanded else OPERATOR(other, self.value)
                unit = self.unit
                name = self.name if not self.constant else None

        elif isinstance(other, tuple(sympy.core.all_classes)):
            other_value, other_unit = Quantity.decompose_expr(other)

            if name == 'add' or name == 'sub':
                if self.unit != other_value:
                    raise UnitError("Addition and subtraction require the same unit.")
                else:
                    unit = self.unit

            else:
                unit = OPERATOR(self.unit, other_unit) if not rhanded else OPERATOR(other_unit, self.unit)

            if name == 'pow':
                raise UnitError("An exponent with one unit is not possible.")

            value = OPERATOR(self.value, other_value) if not rhanded else OPERATOR(other_value, self.value)
            name = self.name if not self.constant else None

        else:
            value = OPERATOR(self.value, other) if not rhanded else OPERATOR(other, self.value)
            unit = self.unit
            name = self.name if not self.constant else None

        dtype = value.dtype
        return self.__create_new_instance(value, unit, name, dtype)

    def __mul__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_OPERATOR(other, OPERATOR)

    def __truediv__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_OPERATOR(other, OPERATOR)

    def __floordiv__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_OPERATOR(other, OPERATOR)

    def __mod__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_OPERATOR(other, OPERATOR)

    __div__ = __truediv__

    def __add__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_OPERATOR(other, OPERATOR)

    def __sub__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_OPERATOR(other, OPERATOR)

    def __pow__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_OPERATOR(other, OPERATOR)

    def __lshift__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR)

    def __rshift__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR)

    def __and__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR)

    def __or__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR)

    def __xor__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR)

    # Right Operations --------------------------------------------------------------------------------
    __rmul__ = __mul__
    __radd__ = __add__

    def __rtruediv__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_OPERATOR(other, OPERATOR, True)

    __rdiv__ = __rtruediv__

    def __rsub__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_OPERATOR(other, OPERATOR, True)

    def __rlshift__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR, True)

    def __rrshift__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR, True)

    def __rfloordiv__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR, True)

    def __rmod__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR, True)

    def __rpow__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR, True)

    def __rand__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR, True)

    def __ror__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR, True)

    def __rxor__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_LOGICAL(other, OPERATOR, True)

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
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_COMPARISON(other, OPERATOR)

    def __ne__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_COMPARISON(other, OPERATOR)

    def __lt__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_COMPARISON(other, OPERATOR)

    def __gt__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_COMPARISON(other, OPERATOR)

    def __le__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_COMPARISON(other, OPERATOR)

    def __ge__(self, other):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        return self.__DO_COMPARISON(other, OPERATOR)

    # --------------------------------------------------------------------------------------------------------
    # Numeric Magic Methods
    # --------------------------------------------------------------------------------------------------------
    def __pos__(self):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        value = OPERATOR(self.value)
        return self.__create_new_instance(value, self.unit, self.name)

    def __neg__(self):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        value = OPERATOR(self.value)
        return self.__create_new_instance(value, self.unit, self.name)

    def __abs__(self):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        value = OPERATOR(self.value)
        return self.__create_new_instance(value, self.unit, self.name)

    def __invert__(self):
        name = __UFUNC_NAME__[inspect.currentframe().f_code.co_name]
        OPERATOR = __OPERATORS__.get(name)

        value = OPERATOR(self.value)
        return self.__create_new_instance(value, self.unit, self.name)

    def __iter__(self):
        def iter_over_value(unit, name):
            for item in self.value:
                yield self.__create_new_instance(item, unit, name)

        return iter_over_value(self.unit, self.name)

    # --------------------------------------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------------------------------------
    @property
    def real(self):
        return self.__create_new_instance(self.value.real, unit=self.unit, name=self.name, dtype=self.value.real.dtype)

    @property
    def imag(self):
        return self.__create_new_instance(self.value.imag, unit=self.unit, name=self.name, dtype=self.value.imag.dtype)

    @property
    def unitstr(self):
        """
        Return the unit of the expression as string.

        Returns
        -------
        unit : str
        """

        if self.unit is None:
            return '-'
        elif self.unit is 1 or self.unit is '1':
            return '-'
        elif isinstance(self.unit, type(One)):
            return '-'
        else:
            return str(self.unit)

    @property
    def math_text(self):
        """
        Return the unit of the expression as math text of form r'$unit$'.

        Returns
        -------
        unit : str
        """

        if self.unit is None:
            return '-'
        elif self.unit is 1 or self.unit is '1':
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

        return self.name + ' ' + '\n' + ' in ' + '[' + self.math_text + ']'

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
    def decompose_expr(expr):
        """
        Extract value and unit from an sympy expression.

        Parameters
        ----------
        expr :sympy.core.mul.Mul
            Sympy expression

        Returns
        -------
        tuple with (values, units)
        """
        copy_value = expr

        if isinstance(copy_value, np.ndarray):
            value, unit = self.__sympy_array(copy_value)

        else:
            value = copy_value.args[0]

            try:
                value = float(value)

                if len(copy_value.args[1:]) > 1:
                    unit = copy_value.args[1]

                    for item in copy_value.args[2:]:
                        unit *= item
                else:
                    unit = copy_value.args[1]

            except TypeError:
                value = 1
                unit = copy_value.as_terms()[0][0][0]

        return value, unit

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
        self.name = name

    def convert_to(self, unit, inplace=False):
        """
        Convert a quantity to another unit.

        Parameters
        ----------
        unit : sympy.physics.units.quantities.Quantity, str
            An object that represents the unit associated with the input value.
            Must be an `sympy.physics.units.quantities.Quantity` object or a string parsable by
            the :mod:`~respy.units` package.
        inplace : bool
            If True the values of the actual class will be overwritten.

        Returns
        -------
        respy.units.Quantity or None

        """
        unit = util.def_unit(unit)

        try:
            dimension = unit.dimension.name

            if dimension == self.dimension:
                scaled_value = self.value.astype(self._dtype) * util.Units[str(dimension)][str(self.unit)].scale_factor
                value = scaled_value / util.Units[str(dimension)][str(unit)].scale_factor

            else:
                value = np.zeros_like(self.value, dtype=self._dtype)

                if len(self.value) == 1:
                    arg = unit_base.convert_to_unit(self.expr, unit)
                    value[0] = arg.base
                    value = value.flatten()

                else:
                    shape = self.value.shape
                    expr = self.expr.flatten()
                    value = unit_base.convert_to_unit(expr, unit)

                    value = value.base
                    value = value.reshape(shape)

            dtype = value.dtype

        except AttributeError:
            value = np.zeros_like(self.value, dtype=self._dtype)

            if len(self.value) == 1:
                arg = unit_base.convert_to_unit(self.expr, unit)
                value[0] = arg.base
                value = value.flatten()

            else:
                shape = self.value.shape
                expr = self.expr.flatten()
                value = unit_base.convert_to_unit(expr, unit)

                value = value.base
                value = value.reshape(shape)

            dtype = value.dtype

        if inplace:
            self.__set_attributes(unit, value, self._dtype, self.copy, self.order, self.subok, False,
                                  self.ndmin, self.dimension)
        else:

            return self.__create_new_instance(value, unit, self.name)

    # --------------------------------------------------------------------------------------------------------
    # Private Methods
    # --------------------------------------------------------------------------------------------------------
    def __get_name(self, other):
        if hasattr(other, 'name'):
            name = self.__compute_name(self.name, other.name, self.constant, other.constant)
        else:
            name = self.name if not self.constant else None

        return name

    def __get_unit(self, other, operator):
        if hasattr(other, 'unit'):
            unit = self.__compute_unit(self.unit, other.unit, operator)
        else:
            unit = self.unit

        return unit

    def __get_value(self, other, operator):
        value = self.value

        if hasattr(other, 'value'):
            other_value = other.value
        else:
            other_value = other

        if operator == "mul" or operator == "rmul":
            result = value * other_value
        elif operator == "div":
            result = value / other_value
        elif operator == "rdiv":
            result = other_value / value
        elif operator == "add" or "radd":
            result = value + other_value
        elif operator == "sub":
            result = value - other_value
        elif operator == "rsub":
            result = other_value - value
        elif operator == "pow":
            result = value ** other_value
        elif operator == "rpow":
            result = other_value ** value
        else:
            raise NotImplementedError("Operation {0} is not implemented.".format(operator))

        return result

    def __compute_unit(self, unit1, unit2, operator):
        if unit1 is None and unit2 is None:
            unit = None
        elif unit1 is None:
            unit = unit2
        elif unit2 is None:
            unit = unit1

        elif unit1 is not None and unit2 is not None:
            if operator == "mul" or operator == "rmul":
                unit = unit1 * unit2
            elif operator == "div":
                unit = unit1 / unit2
            elif operator == "rdiv":
                unit = unit2 / unit1
            elif operator == "add" or "radd":
                unit = unit1 + unit2
            elif operator == "sub":
                unit = unit1 - unit2
            elif operator == "rsub":
                unit = unit2 - unit1
            elif operator == "pow":
                unit = unit1 ** unit2
            else:
                raise NotImplementedError("Operation {0} is not implemented.".format(operator))
        else:
            raise RuntimeError("Could not calculate unit.")

        return unit

    def __compute_name(self, name1, name2, const1, const2):
        if name1 is None and name2 is None:
            name = None

        elif name1 is None:
            if const2:
                name = name1
            else:
                name = name2

        elif name2 is None:
            if const1:
                name = name2
            else:
                name = name1

        elif name1 is not None and name2 is not None:
            if name1 == name2:
                name = name1
            else:
                name = None
        else:
            raise RuntimeError("Could not calculate name")

        return name

    def __set_attributes(self, unit, value, dtype, copy, order, subok, constant, ndmin):
        if unit is None or isinstance(unit, type(One)):
            self.unit = None
        else:
            self.unit = util.def_unit(unit)

        self.value = value
        self._dtype = dtype
        self.copy = copy
        self.order = order
        self.subok = subok
        self.constant = constant
        self.ndmin = ndmin

        try:
            self.dimension = self.unit.dimension.name
        except AttributeError:
            self.dimension = None

    def __create_new_instance(self, value, unit=None, name=None, dtype=None):

        quantity_subclass = self.__class__

        if unit is None or unit is 1:
            unit = None
        elif isinstance(unit, type(One)):
            unit = None
        else:
            pass

        if dtype is None:
            dtype = self._dtype
        else:
            pass

        value = np.array(value, dtype=dtype, copy=False, order=self.order,
                         subok=self.subok)

        value = np.atleast_1d(value)
        view = value.view(quantity_subclass)

        view.__set_attributes(unit, value, dtype, self.copy, self.order, self.subok, self.constant, self.ndmin)
        view.set_name(name)

        return view
