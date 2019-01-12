import numpy as np
import respy.units.util as util
import sympy
from sympy.physics.units import convert_to


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
        obj = x.view(type=cls)

        if unit is None:
            obj._unit = unit

        else:
            obj._unit = util.def_unit(unit)

        value = np.atleast_1d(np.asarray(value))
        obj._value = value
        obj._name = name
        obj._constant = constant

        return obj

    # --------------------------------------------------------------------------------------------------------
    # Magic Methods
    # --------------------------------------------------------------------------------------------------------
    def __repr__(self):
        if self._name is None:
            prefix = '<{0} '.format(self.__class__.__name__)
            sep = ','
            arrstr = np.array2string(self.view(np.ndarray),
                                     separator=sep,
                                     prefix=prefix)

            return '{0}{1} [{2}]>'.format(prefix, arrstr, self.unitstr)

        else:
            prefix = '<{0} '.format(self.__class__.__name__)
            sep = ','
            arrstr = np.array2string(self.view(np.ndarray),
                                     separator=sep,
                                     prefix=prefix)

            return '{0}{1} {2} in [{3}]>'.format(prefix, arrstr, self._name, self.unitstr)

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self._unit = getattr(obj, 'unitstr', None)
        self._value = getattr(obj, '_value', None)
        self._name = getattr(obj, '_name', None)
        self._constant = getattr(obj, '_constant', None)

    # --------------------------------------------------------------------------------------------------------
    # Operator
    # --------------------------------------------------------------------------------------------------------
    def __mul__(self, other):
        if isinstance(other, tuple(sympy.core.all_classes)):
            value, unit = self.__check_sympy_expr(other)
            obj = self.value * value
            unit = self.__select_unit(self.unit, unit, 'mul')
            name = self.__select_name(self._name, None, self._constant, None, 'mul')

            return self.__create_new_instance(obj, unit, name)

        elif isinstance(other, Quantity):
            obj = self.value * other.value
            unit = self.__select_unit(self.unit, other.unit, 'mul')
            name = self.__select_name(self._name, other._name, self._constant, other._constant, 'mul')

            return self.__create_new_instance(obj, unit, name)

        else:
            obj = self.value * other
            unit = self.unit

            return self.__create_new_instance(obj, unit, self._name)

    def __rmul__(self, other):
        if isinstance(other, tuple(sympy.core.all_classes)):
            value, unit = self.__check_sympy_expr(other)
            obj = self.value * value
            unit = self.__select_unit(self.unit, unit, 'rmul')
            name = self.__select_name(self._name, None, self._constant, None, 'rmul')

            return self.__create_new_instance(obj, unit, name)

        elif isinstance(other, Quantity):
            obj = self.value * other.value
            unit = self.__select_unit(self.unit, other.unit, 'rmul')
            name = self.__select_name(self._name, other._name, self._constant, other._constant, 'rmul')

            return self.__create_new_instance(obj, unit, name)

        else:
            obj = self.value * other
            unit = self.unit

            return self.__create_new_instance(obj, unit, self._name)

    def __div__(self, other):
        if isinstance(other, tuple(sympy.core.all_classes)):
            value, unit = self.__check_sympy_expr(other)
            obj = self.value / value
            unit = self.__select_unit(self.unit, unit, 'div')
            name = self.__select_name(self._name, None, self._constant, None, 'div')

            return self.__create_new_instance(obj, unit, name)

        elif isinstance(other, Quantity):
            obj = self.value / other.value
            unit = self.__select_unit(self.unit, other.unit, 'div')
            name = self.__select_name(self._name, other._name, self._constant, other._constant, 'div')

            return self.__create_new_instance(obj, unit, name)

        else:
            obj = self.value / other
            unit = self.unit

            return self.__create_new_instance(obj, unit, self._name)

    def __rdiv__(self, other):
        if isinstance(other, tuple(sympy.core.all_classes)):
            value, unit = self.__check_sympy_expr(other)
            obj = value / self.value
            unit = self.__select_unit(self.unit, unit, 'rdiv')
            name = self.__select_name(self._name, None, self._constant, None, 'rdiv')

            return self.__create_new_instance(obj, unit, name)

        elif isinstance(other, Quantity):
            obj = other.value / self.value
            unit = self.__select_unit(self.unit, other.unit, 'rdiv')
            name = self.__select_name(self._name, other._name, self._constant, other._constant, 'rdiv')

            return self.__create_new_instance(obj, unit, name)

        else:
            obj = other.value / self.value
            unit = self.unit

            return self.__create_new_instance(obj, unit, self._name)

    def __add__(self, other):
        if isinstance(other, tuple(sympy.core.all_classes)):
            value, unit = self.__check_sympy_expr(other)
            obj = self.value + value
            unit = self.__select_unit(self.unit, unit, 'add')
            name = self.__select_name(self._name, None, self._constant, None, 'add')

            return self.__create_new_instance(obj, unit, name)

        elif isinstance(other, Quantity):
            obj = self.value + other.value
            unit = self.__select_unit(self.unit, other.unit, 'add')
            name = self.__select_name(self._name, other._name, self._constant, other._constant, 'add')

            return self.__create_new_instance(obj, unit, name)

        else:
            obj = self.value + other
            unit = self.unit

            return self.__create_new_instance(obj, unit, self._name)

    def __radd__(self, other):
        if isinstance(other, tuple(sympy.core.all_classes)):
            value, unit = self.__check_sympy_expr(other)
            obj = self.value + value
            unit = self.__select_unit(self.unit, unit, 'radd')
            name = self.__select_name(self._name, None, self._constant, None, 'radd')

            return self.__create_new_instance(obj, unit, name)

        elif isinstance(other, Quantity):
            obj = self.value + other.value
            unit = self.__select_unit(self.unit, other.unit, 'radd')
            name = self.__select_name(self._name, other._name, self._constant, other._constant, 'radd')

            return self.__create_new_instance(obj, unit, name)

        else:
            obj = self.value + other
            unit = self.unit

            return self.__create_new_instance(obj, unit, self._name)

    def __sub__(self, other):
        if isinstance(other, tuple(sympy.core.all_classes)):
            value, unit = self.__check_sympy_expr(other)
            obj = self.value - value
            unit = self.__select_unit(self.unit, unit, 'sub')
            name = self.__select_name(self._name, None, self._constant, None, 'sub')

            return self.__create_new_instance(obj, unit, name)

        elif isinstance(other, Quantity):
            obj = self.value - other.value
            unit = self.__select_unit(self.unit, other.unit, 'sub')
            name = self.__select_name(self._name, other._name, self._constant, other._constant, 'sub')

            return self.__create_new_instance(obj, unit, name)

        else:
            obj = self.value - other
            unit = self.unit

            return self.__create_new_instance(obj, unit, self._name)

    def __rsub__(self, other):
        if isinstance(other, tuple(sympy.core.all_classes)):
            value, unit = self.__check_sympy_expr(other)
            obj = value - self.value
            unit = self.__select_unit(self.unit, unit, 'rsub')
            name = self.__select_name(self._name, None, self._constant, None, 'rsub')

            return self.__create_new_instance(obj, unit, name)

        elif isinstance(other, Quantity):
            obj = other.value - self.value
            unit = self.__select_unit(self.unit, other.unit, 'rsub')
            name = self.__select_name(self._name, other._name, self._constant, other._constant, 'rsub')

            return self.__create_new_instance(obj, unit, name)

        else:
            obj = other.value - self.value
            unit = self.unit

            return self.__create_new_instance(obj, unit, self._name)

    # --------------------------------------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------------------------------------
    @property
    def unit(self):
        """
        Return the unit of the expression.

        Returns
        -------
        unit : sympy.physics.units.quantities.Quantity
        """
        return self._unit

    @property
    def value(self):
        """
        Return the numerical value of the expression.

        Returns
        -------
        value : numpy.ndarray
        """
        return self._value

    @property
    def unitstr(self):
        """
        Return the unit of the expression as string.

        Returns
        -------
        unit : str
        """
        if self._unit is None:
            return "-"
        else:
            return str(self._unit)

    @property
    def expr(self):
        """
        Return the expression.

        Returns
        -------
        expr : numpy.ndarray with sympy.core.mul.Mul
        """
        return self._value * self._unit

    # --------------------------------------------------------------------------------------------------------
    # Callable Methods
    # --------------------------------------------------------------------------------------------------------
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
        respy.units.Quantity

        """
        unit = util.def_unit(unit)

        if len(self._value) == 1:
            value = convert_to(self.expr[0], unit).n()

        else:
            value = np.zeros_like(self._value, dtype=np.float)
            shape = value.shape

            value = value.flatten()
            expr = self.expr.flatten()

            for i, item in enumerate(value):
                arg = convert_to(expr[i], unit).n()
                value[i] = arg.args[0]

            value = value.reshape(shape)

        return self.__create_new_instance(value, unit, self._name)

    # --------------------------------------------------------------------------------------------------------
    # Private Methods
    # --------------------------------------------------------------------------------------------------------
    def __check_sympy_expr(self, expr):
        copy_value = expr
        value = copy_value.args[0]

        if len(copy_value.args[1:]) > 1:
            unit = copy_value.args[1]

            for item in copy_value.args[2:]:
                unit *= item
        else:
            unit = copy_value.args[1]

        return value, unit

    def __select_unit(self, unit1, unit2, operator):
        if unit2 is None:
            unit = unit1
        elif unit1 is None:
            unit = unit2
        else:
            if operator == 'mul' or operator == 'rmul':
                unit = unit1 * unit2
            elif operator == 'div':
                unit = unit1 / unit2
            elif operator == 'rdiv':
                unit = unit2 / unit1
            elif operator == 'add' or operator == 'radd':
                unit = unit1 + unit2
            elif operator == 'sub':
                unit = unit1 - unit2
            elif operator == "rsub":
                unit = unit2 - unit1
            else:
                unit = None

        return unit

    def __select_name(self, name1, name2, constant1, constant2, operator):
        if name1 is None and name2 is None:
            name = None

        elif name1 == name2:
            if constant1 or constant2:
                name = None
            else:
                name = name1

        elif name1 is None and name2 is not None:
            if constant1 or constant2:
                name = None
            else:
                name = name2
        elif name1 is not None and name2 is None:
            if constant1 or constant2:
                name = None
            else:
                name = name1

        elif name1 is not None and name2 is not None:

            if operator == 'mul':
                if constant1:
                    name = name2
                elif constant2:
                    name = name1
                elif constant1 and constant2:
                    name = None
                else:
                    name = self.__operator_name(name1, name2, ' * ')

            elif operator == 'rmul':
                if constant1:
                    name = name2
                elif constant2:
                    name = name1
                elif constant1 and constant2:
                    name = None
                else:
                    name = self.__operator_name(name1, name2, ' * ', True)

            elif operator == 'div':
                if constant1:
                    name = name2
                elif constant2:
                    name = name1
                elif constant1 and constant2:
                    name = None
                else:
                    name = self.__operator_name(name1, name2, ' / ')

            elif operator == 'rdiv':
                if constant1:
                    name = name2
                elif constant2:
                    name = name1
                elif constant1 and constant2:
                    name = None
                else:
                    name = self.__operator_name(name1, name2, ' / ', True)

            elif operator == 'add':
                if constant1:
                    name = name2
                elif constant2:
                    name = name1
                elif constant1 and constant2:
                    name = None
                else:
                    name = self.__operator_name(name1, name2, ' + ')

            elif operator == 'radd':
                if constant1:
                    name = name2
                elif constant2:
                    name = name1
                elif constant1 and constant2:
                    name = None
                else:
                    name = self.__operator_name(name1, name2, ' + ', True)

            elif operator == 'sub':
                if constant1:
                    name = name2
                elif constant2:
                    name = name1
                elif constant1 and constant2:
                    name = None
                else:
                    name = self.__operator_name(name1, name2, ' - ')

            elif operator == 'rsub':
                if constant1:
                    name = name2
                elif constant2:
                    name = name1
                elif constant1 and constant2:
                    name = None
                else:
                    name = self.__operator_name(name1, name2, ' - ', True)

            elif operator == 'pow':
                if constant1:
                    name = name2
                elif constant2:
                    name = name1
                elif constant1 and constant2:
                    name = None
                else:
                    name = self.__operator_name(name1, name2, ' ** ')

            else:
                name = None
        else:
            name = None

        return name

    def __operator_name(self, name1, name2, operator, zorder=False):
        if not zorder:
            return name1 + operator + name2
        else:
            return name2 + operator + name1

    def __set_unit(self, unit):
        if unit is None:
            self._unit = unit

        else:
            self._unit = util.def_unit(unit)

    def __set_value(self, value):
        self._value = value

    def __create_new_instance(self, obj, unit=None, name=None):
        quantity_subclass = self.__class__

        if unit is None:
            unit = self.unit

        obj = np.array(obj, copy=False)
        view = obj.view(quantity_subclass)
        view.__set_unit(unit)
        view.__set_value(obj)
        view.set_name(name)

        return view


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
