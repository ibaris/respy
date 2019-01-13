from __future__ import division
import numpy as np
from respy.units import util as util
import respy
import sympy
from sympy.physics.units import convert_to
import sys

__STR_OPERAND__ = {'mul': ' * ',
                   'div': ' / ',
                   'add': ' + ',
                   'sub': ' - ',
                   'pow': ' ** '}


class Quantity(np.ndarray):
    def __new__(cls, value, unit=None, dtype=None, copy=True, order=None,
                subok=False, ndmin=0, name=None, constant=False):
        """
        The Quantity object is meant to represent a value that has some unit associated with the number.

        Parameters
        ----------
        value : float, int, numpy.ndarray, str, sympy.core.mul.Mul
            The numerical value of this quantity in the units given by unit.

        unit : sympy.physics.units.quantities.Quantity, str
            An object that represents the unit associated with the input value.
            Must be an `sympy.physics.units.quantities.Quantity` object or a string parsable by
            the :mod:`~respy.units` package.

        dtype : numpy.dtype, optional
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

        Returns
        -------

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

        obj = x.view(type=cls)

        if unit is None:
            obj.unit = None
        else:
            obj.unit = util.def_unit(unit)

        obj.value = x
        obj.name = name
        obj.constant = constant

        obj.dtype = dtype
        obj.copy = copy
        obj.order = order
        obj.subok = subok
        obj.ndmin = ndmin

        return obj

    # --------------------------------------------------------------------------------------------------------
    # Magic Methods
    # --------------------------------------------------------------------------------------------------------
    def __repr__(self):
        if self.name is None:
            prefix = '<{0} '.format(self.__class__.__name__)
            sep = ','
            arrstr = np.array2string(self.value,
                                     separator=sep,
                                     prefix=prefix)

            return '{0}{1} [{2}]>'.format(prefix, arrstr, self.unitstr)

        else:
            prefix = '<{0} '.format(self.__class__.__name__)
            sep = ','
            arrstr = np.array2string(self.value,
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
            self.dtype = getattr(obj, 'dtype', None)
            self.copy = getattr(obj, 'copy', None)
            self.order = getattr(obj, 'order', None)
            self.subok = getattr(obj, 'subok', None)
            self.ndmin = getattr(obj, 'ndmin', None)

    # --------------------------------------------------------------------------------------------------------
    # Operator
    # --------------------------------------------------------------------------------------------------------
    def __mul__(self, other):
        operator = 'mul'
        if isinstance(other, (self.__class__, respy.units.quantity.Quantity, np.ndarray)):
            unit = self.__get_unit(other, operator)
            value = self.__get_value(other, operator)
            name = self.__get_name(other, operator)

            return self.__create_new_instance(value, unit, name)

        elif isinstance(other, tuple(sympy.core.all_classes)):
            other_value, other_unit = Quantity.extract_from_expr(other)
            value = self.value * other_value
            unit = self.__compute_unit(self.unit, other_unit, operator)
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

        else:
            value = self.value * other
            unit = self.unit
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

    __rmul__ = __imul__ = __mul__

    def __truediv__(self, other):
        operator = 'div'
        if isinstance(other, (self.__class__, respy.units.quantity.Quantity, np.ndarray)):
            unit = self.__get_unit(other, operator)
            value = self.__get_value(other, operator)
            name = self.__get_name(other, operator)

            return self.__create_new_instance(value, unit, name)

        elif isinstance(other, tuple(sympy.core.all_classes)):
            other_value, other_unit = Quantity.extract_from_expr(other)
            value = self.value / other_value
            unit = self.__compute_unit(self.unit, other_unit, operator)
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

        else:
            value = self.value / other
            unit = self.unit
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

    def __rtruediv__(self, other):
        operator = 'rdiv'
        if isinstance(other, (self.__class__, respy.units.quantity.Quantity, np.ndarray)):
            unit = self.__get_unit(other, operator)
            value = self.__get_value(other, operator)
            name = self.__get_name(other, operator)

            return self.__create_new_instance(value, unit, name)

        elif isinstance(other, tuple(sympy.core.all_classes)):
            other_value, other_unit = Quantity.extract_from_expr(other)
            value = other_value / self.value
            unit = self.__compute_unit(self.unit, other_unit, operator)
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

        else:
            value = other / self.value
            unit = self.unit
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

    __div__ = __idiv__ = __itruediv__ = __truediv__
    __rdiv__ = __rtruediv__

    def __add__(self, other):
        operator = 'add'
        if isinstance(other, (self.__class__, respy.units.quantity.Quantity, np.ndarray)):
            unit = self.__get_unit(other, operator)
            value = self.__get_value(other, operator)
            name = self.__get_name(other, operator)

            return self.__create_new_instance(value, unit, name)

        elif isinstance(other, tuple(sympy.core.all_classes)):
            other_value, other_unit = Quantity.extract_from_expr(other)
            value = self.value + other_value
            unit = self.__compute_unit(self.unit, other_unit, operator)
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

        else:
            value = self.value + other
            unit = self.unit
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

    __radd__ = __add__

    def __sub__(self, other):
        operator = 'sub'
        if isinstance(other, (self.__class__, respy.units.quantity.Quantity, np.ndarray)):
            unit = self.__get_unit(other, operator)
            value = self.__get_value(other, operator)
            name = self.__get_name(other, operator)

            return self.__create_new_instance(value, unit, name)

        elif isinstance(other, tuple(sympy.core.all_classes)):
            other_value, other_unit = Quantity.extract_from_expr(other)
            value = self.value - other_value
            unit = self.__compute_unit(self.unit, other_unit, operator)
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

        else:
            value = self.value - other
            unit = self.unit
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

    def __rsub__(self, other):
        operator = 'sub'
        if isinstance(other, (self.__class__, respy.units.quantity.Quantity, np.ndarray)):
            unit = self.__get_unit(other, operator)
            value = self.__get_value(other, operator)
            name = self.__get_name(other, operator)

            return self.__create_new_instance(value, unit, name)

        elif isinstance(other, tuple(sympy.core.all_classes)):
            other_value, other_unit = Quantity.extract_from_expr(other)
            value = other_value - self.value
            unit = self.__compute_unit(self.unit, other_unit, operator)
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

        else:
            value = other - self.value
            unit = self.unit
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

    def __pow__(self, other):
        operator = 'pow'
        if isinstance(other, (self.__class__, respy.units.quantity.Quantity, np.ndarray)):
            unit = self.__get_unit(other, operator)
            value = self.__get_value(other, operator)
            name = self.__get_name(other, operator)

            return self.__create_new_instance(value, unit, name)

        elif isinstance(other, tuple(sympy.core.all_classes)):
            other_value, other_unit = Quantity.extract_from_expr(other)
            value = self.value ** other_value
            unit = self.__compute_unit(self.unit, other_unit, operator)
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

        else:
            value = self.value ** other
            unit = self.unit
            name = self.name if not self.constant else None

            return self.__create_new_instance(value, unit, name)

    # --------------------------------------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------------------------------------
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
        else:
            return str(self.unit)

    @property
    def expr(self):
        """
        Return the expression.

        Returns
        -------
        expr : numpy.ndarray with sympy.core.mul.Mul
        """
        return self.value * self.unit

    # --------------------------------------------------------------------------------------------------------
    # Callable Methods
    # --------------------------------------------------------------------------------------------------------
    @staticmethod
    def extract_from_expr(expr):
        copy_value = expr
        value = copy_value.args[0]

        if len(copy_value.args[1:]) > 1:
            unit = copy_value.args[1]

            for item in copy_value.args[2:]:
                unit *= item
        else:
            unit = copy_value.args[1]

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

        Returns
        -------
        respy.units.Quantity

        """
        unit = util.def_unit(unit)
        value = np.zeros_like(self.value, dtype=self.dtype)

        if len(self.value) == 1:
            arg = convert_to(self.expr[0], unit).n()
            value[0] = arg.args[0]
            value = value.flatten()

        else:
            value = np.zeros_like(self.value, dtype=self.dtype)
            shape = value.shape

            value = value.flatten()
            expr = self.expr.flatten()

            for i, item in enumerate(value):
                arg = convert_to(expr[i], unit).n()
                value[i] = arg.args[0]

            value = value.reshape(shape)

        if inplace:
            self.__set_attributes(unit, value, self.dtype, self.copy, self.order, self.subok, False, self.ndmin)
        else:
            return self.__create_new_instance(value, unit, self.name)

    # --------------------------------------------------------------------------------------------------------
    # Private Methods
    # --------------------------------------------------------------------------------------------------------
    def __get_name(self, other, operator):
        if hasattr(other, 'name'):
            name = self.__compute_name(self.name, other.name, self.constant, other.constant, operator)
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
                unit = pow(unit1, unit2)
            else:
                raise NotImplementedError("Operation {0} is not implemented.".format(operator))
        else:
            raise RuntimeError("Could not calculate unit.")

        return unit

    def __compute_name(self, name1, name2, const1, const2, operator):
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
            if const1 and const2:
                name = None
            elif const1:
                name = name2
            elif const2:
                name = name1
            else:
                name = name1 + __STR_OPERAND__[operator] + name2
        else:
            raise RuntimeError("Could not calculate name")

        return name

    def __set_attributes(self, unit, value, dtype, copy, order, subok, constant, ndmin):
        self.unit = util.def_unit(unit)
        self.value = value
        self.dtype = dtype
        self.copy = copy
        self.order = order
        self.subok = subok
        self.constant = constant
        self.ndmin = ndmin

    def __create_new_instance(self, value, unit=None, name=None):

        quantity_subclass = self.__class__

        if unit is None:
            unit = "-"

        if self.ndmin is None:
            ndmin = 0
        else:
            ndmin = self.ndmin

        value = np.array(value, dtype=self.dtype, copy=False, order=self.order,
                         subok=self.subok)

        view = value.view(quantity_subclass)
        view.__set_attributes(unit, value, self.dtype, self.copy, self.order, self.subok, False, self.ndmin)
        view.set_name(name)

        return view

# #
import respy.constants as const

F = Quantity(1.26, unit="GHz")
# fh = F.convert_to('1 / s')
#
# w = const.c / fh
# w.convert_to('cm')

# a = 2345 * 1/util.s
#
# a = const.c * F
# a.unit
# unit = "joule / kelvin * meter / seconds"

# array = np.array([[2, 2, 3, 4], [5, 6, 7, 8]])
#
# q = Quantity(array, name='q', unit="meter / second")
# u = Quantity(0.25, name='u', unit='seconds')
#
# v = Quantity(array, name='BSC')
# x = Quantity(array, name='BRDF', constant=True)
#
# t = Quantity(30, unit='meter')
# a = 2 * util.cm * 5 * util.m / util.K * 45 * util.J
# # z = Quantity(a)

# f = Quantity(array, unit='GHz')
