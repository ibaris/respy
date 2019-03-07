from __future__ import division

import numpy as np
import pytest

from respy.units import Quantity
from respy.units.auxil import __NONE_UNITS__
from respy import units
import respy

import random
import operator
from respy.units import Zero
from respy.units import dimensions

#
a = Quantity(53, unit='1 / s')
av = Quantity(53, unit='cm', verbose=True)
b = Quantity(2.5, unit='m / s')
bc = b.convert_to('cm')
self = a
other = bc

__MATH_UNIT_GETS_LOST__ = {"signbit": np.signbit,
                           "mod": np.mod,
                           "fmod": np.fmod,
                           "divmod": np.divmod,
                           "logaddexp": np.logaddexp,
                           "logaddexp2": np.logaddexp2,
                           "sign": np.sign,
                           "heaviside": np.heaviside,
                           "exp": np.exp,
                           "exp2": np.exp2,
                           "log": np.log,
                           "log2": np.log2,
                           "log10": np.log10,
                           "expm1": np.expm1,
                           "log1p": np.log1p,
                           "sin": np.sin,
                           "cos": np.cos,
                           "tan": np.tan,
                           "arcsin": np.arcsin,
                           "arccos": np.arccos,
                           "arctan": np.arctan,
                           "arctan2": np.arctan2,
                           "hypot": np.hypot,
                           "sinh": np.sinh,
                           "cosh": np.cosh,
                           "tanh": np.tanh,
                           "arcsinh": np.arcsinh,
                           "arccosh": np.arccosh,
                           "arctanh": np.arctanh,
                           "deg2rad": np.deg2rad,  # Special CASE
                           "rad2deg": np.rad2deg,  # Special CASE
                           "bitwise_and": np.bitwise_and,
                           "bitwise_or": np.bitwise_or,
                           "bitwise_xor": np.bitwise_xor,
                           "invert": np.invert,
                           "left_shift": np.left_shift,
                           "right_shift": np.right_shift}

__MATH_UNIT_REMAINS_STABLE__ = {"absolute": np.absolute,
                                "fabs": np.fabs,
                                "negative": np.negative,
                                "positive": np.positive,
                                "rint": np.rint,
                                "conj": np.conj,
                                "conjugate": np.conjugate,
                                "nan_to_num": np.nan_to_num}


# c = Quantity(3, unit='m')
#
# a * a


class TestInput:
    def test_input_plain(self):
        value = 23
        unit = 'GHz'
        name = 'Test Case'
        q = Quantity(value=value, unit=unit, name=name)

        assert (q.name == name)
        assert (q.dimension == dimensions.frequency)
        assert (q.dtype == float)
        assert (q.unitstr == str(respy.units.Units.frequency[unit]))
        assert (q.value == value)
        # assert (repr(q) == '<Quantity [23.] Test Case in [gigahertz]>')

    def test_input_none(self):
        value = 23
        name = 'Test Case'
        q = Quantity(value=value, name='Test Case')

        assert (q.name == name)
        assert (q.dimension == Zero)
        assert (q.dtype == float)
        assert (q.unitstr == '-')
        assert (q.value == value)
        # assert (repr(q) == '<Quantity [23.] Test Case in [-]>')

    def test_input_no_name(self):
        value = 23
        unit = 'GHz'
        q = Quantity(value=value, unit=unit)

        assert (q.name is None)
        assert (q.dimension == dimensions.frequency)
        assert (q.dtype == float)
        assert (q.unitstr == str(respy.units.Units.frequency[unit]))
        assert (q.value == value)
        # assert (repr(q) == '<Quantity [23.] [gigahertz]>')

    def test_input_all_array(self):

        value = np.linspace(1, 100, 10)
        unit = 'meter'
        name = 'Test Case Array'
        q = Quantity(value=value, unit=unit, name=name)

        assert (q.name == name)
        assert (q.dimension == dimensions.length)
        assert (q.dtype == float)
        assert (q.unitstr == str(respy.units.Units.length[unit]))
        assert (np.all(q.value == value))
        # assert (repr(
        #     q) == '<Quantity [  1.,  12.,  23.,  34.,  45.,  56.,  67.,  78.,  89., 100.] Test Case Array in [meter]>')

    def test_input_dimension(self):
        value = np.linspace(0, 20, 5)

        for item in respy.units.Units.frequency.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (q.dimension == dimensions.frequency)
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.frequency[item]))
            assert (np.all(q.value == value))
            # assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.frequency[item]))

        for item in respy.units.Units.length.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (q.dimension == dimensions.length)
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.length[item]))
            assert (np.all(q.value == value))
            # assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.length[item]))

        for item in respy.units.Units.other.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (q.dimension == Zero)
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.other[item]))
            assert (np.all(q.value == value))
            # assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.other[item]))

        for item in respy.units.Units.temperature.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (q.dimension == dimensions.temperature)
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.temperature[item]))
            assert (np.all(q.value == value))
            # assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.temperature[item]))

        for item in respy.units.Units.time.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (q.dimension == dimensions.time)
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.time[item]))
            assert (np.all(q.value == value))
            # assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.time[item]))

        for item in respy.units.Units.energy.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (q.dimension == dimensions.energy)
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.energy[item]))
            assert (np.all(q.value == value))
            # assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.energy[item]))


ops = {'+': operator.add,
       '-': operator.sub,
       '*': operator.mul,
       '/': operator.truediv}

unit = [units.m, 1 / units.m, units.m ** 2, 1 / units.m ** 2]
#
a, b, c, d, a_unit, b_unit, c_unit, d_unit = (
np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
unit[np.random.randint(0, 3)])


@pytest.mark.webtest
@pytest.mark.parametrize("a, b, c, d, a_unit, b_unit, c_unit, d_unit", [
    (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
     unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
     unit[np.random.randint(0, 3)]),
    (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
     unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
     unit[np.random.randint(0, 3)]),
    (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
     unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
     unit[np.random.randint(0, 3)]),
    (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
     unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
     unit[np.random.randint(0, 3)])
])
class TestOperation:
    def test_operation_unit(self, a, b, c, d, a_unit, b_unit, c_unit, d_unit):
        test_list = [a, b, c, d]
        unit_list = [a_unit, b_unit, c_unit, d_unit]

        for i in range(100):
            op = random.choice(list(ops.keys()))

            item1_value = random.choice(test_list)
            item2_value = random.choice(test_list)

            unit1 = random.choice(unit_list)
            unit2 = unit1

            unit1_temp = item1_value * unit1
            unit2_temp = item2_value * unit2

            item1 = Quantity(item1_value, unit=unit1)
            item2 = Quantity(item2_value, unit=unit2)

            test = ops.get(op)(item1, item2)
            ref = ops.get(op)(unit1_temp, unit2_temp)

            assert np.allclose(test.value, ops.get(op)(item1_value, item2_value))

            try:
                assert test.unit == ref[0].as_coeff_mul()[1][1]
            except IndexError:
                pass


@pytest.mark.webtest
@pytest.mark.parametrize("a, b, c, d, a_unit, b_unit, c_unit, d_unit", [
    (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
     unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
     unit[np.random.randint(0, 3)]),
    (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
     unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
     unit[np.random.randint(0, 3)]),
    (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
     unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
     unit[np.random.randint(0, 3)]),
    (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
     unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
     unit[np.random.randint(0, 3)])
])
class TestUfunc:
    def test_ufunc_unit_gets_lost(self, a, b, c, d, a_unit, b_unit, c_unit, d_unit):
        test_list = [a, b, c, d]
        unit_list = [a_unit, b_unit, c_unit, d_unit]

        for item in __MATH_UNIT_GETS_LOST__.keys():
            item1_value = random.choice(test_list)
            item2_value = random.choice(test_list)

            unit1 = random.choice(unit_list)
            unit2 = unit1

            item1 = Quantity(item1_value, unit=unit1)
            item2 = Quantity(item2_value, unit=unit2)
            function = __MATH_UNIT_GETS_LOST__[item]

            try:
                ufunc = function(item1)
                out = function(item1_value)

                if np.all(np.isnan(out) == True):
                    assert np.all(np.isnan(out) == True) == np.all(np.isnan(ufunc.value) == True)
                else:
                    assert np.all(ufunc.value == out)
                    assert ufunc.unit in __NONE_UNITS__

            except TypeError:

                try:
                    ufunc = function(item1, item2)

                    if function.nout == 2:
                        for i in range(2):
                            assert np.all(ufunc[i].value == function(item1_value, item2_value)[i])
                            assert ufunc[i].unit in __NONE_UNITS__

                    else:
                        assert np.all(ufunc.value == function(item1_value, item2_value))
                        assert ufunc.unit in __NONE_UNITS__

                except (TypeError, AttributeError):
                    pass

    def test_ufunc_unit_is_stable(self, a, b, c, d, a_unit, b_unit, c_unit, d_unit):
        test_list = [a, b, c, d]
        unit_list = [a_unit, b_unit, c_unit, d_unit]

        for item in __MATH_UNIT_REMAINS_STABLE__.keys():
            item1_value = random.choice(test_list)
            item2_value = random.choice(test_list)

            unit1 = random.choice(unit_list)
            unit2 = unit1

            item1 = Quantity(item1_value, unit=unit1)
            item2 = Quantity(item2_value, unit=unit2)
            function = __MATH_UNIT_REMAINS_STABLE__[item]

            try:
                ufunc = function(item1)
                out = function(item1_value)

                if np.all(np.isnan(out) == True):
                    assert np.all(np.isnan(out) == True) == np.all(np.isnan(ufunc.value) == True)
                else:
                    assert np.all(ufunc.value == out)
                    assert ufunc.unit == unit1

            except TypeError:

                try:
                    ufunc = function(item1, item2)

                    if function.nout == 2:
                        for i in range(2):
                            assert np.all(ufunc[i].value == function(item1_value, item2_value)[i])
                            assert ufunc[i].unit in __NONE_UNITS__

                    else:
                        assert np.all(ufunc.value == function(item1_value, item2_value))
                        assert ufunc.unit in __NONE_UNITS__

                except (TypeError, AttributeError):
                    pass