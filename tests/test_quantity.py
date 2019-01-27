from __future__ import division

import numpy as np
import pytest

from respy.units import Quantity
from respy import units
import respy

import random
import operator
from respy.units import Zero, One

a = Quantity(5, unit='cm')
b = Quantity(2.5, unit='cm')
c = Quantity(3, unit='m')

a * a


class TestInput:
    def test_input_plain(self):
        value = 23
        unit = 'GHz'
        name = 'Test Case'
        q = Quantity(value=value, unit=unit, name=name)

        assert (q.name == name)
        assert (str(q.dimension) == 'frequency')
        assert (q.dtype == float)
        assert (q.unitstr == str(respy.units.Units.frequency[unit]))
        assert (q.value == value)
        assert (repr(q) == '<Quantity [23.] Test Case in [gigahertz]>')

    def test_input_none(self):
        value = 23
        name = 'Test Case'
        q = Quantity(value=value, name='Test Case')

        assert (q.name == name)
        assert (q.dimension == Zero)
        assert (q.dtype == float)
        assert (q.unitstr == '-')
        assert (q.value == value)
        assert (repr(q) == '<Quantity [23.] Test Case in [-]>')

    def test_input_no_name(self):
        value = 23
        unit = 'GHz'
        q = Quantity(value=value, unit=unit)

        assert (q.name is b'')
        assert (str(q.dimension) == 'frequency')
        assert (q.dtype == float)
        assert (q.unitstr == str(respy.units.Units.frequency[unit]))
        assert (q.value == value)
        assert (repr(q) == '<Quantity [23.] [gigahertz]>')

    def test_input_all_array(self):

        value = np.linspace(1, 100, 10)
        unit = 'meter'
        name = 'Test Case Array'
        q = Quantity(value=value, unit=unit, name=name)

        assert (q.name == name)
        assert (str(q.dimension) == 'length')
        assert (q.dtype == float)
        assert (q.unitstr == str(respy.units.Units.length[unit]))
        assert (np.all(q.value == value))
        assert (repr(
            q) == '<Quantity [  1.,  12.,  23.,  34.,  45.,  56.,  67.,  78.,  89., 100.] Test Case Array in [meter]>')

    def test_input_dimension(self):
        value = np.linspace(0, 20, 5)

        for item in respy.units.Units.frequency.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is b'')
            assert (str(q.dimension) == 'frequency')
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.frequency[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.frequency[item]))

        for item in respy.units.Units.length.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is b'')
            assert (str(q.dimension) == 'length')
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.length[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.length[item]))

        for item in respy.units.Units.other.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is '')
            assert (q.dimension == One)
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.other[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.other[item]))

        for item in respy.units.Units.temperature.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is b'')
            assert (str(q.dimension) == 'temperature')
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.temperature[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.temperature[item]))

        for item in respy.units.Units.time.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is b'')
            assert (str(q.dimension) == 'time')
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.time[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.time[item]))

        for item in respy.units.Units.energy.keys():
            unit = item
            q = Quantity(value=value, unit=unit)
            assert (q.name is '')
            assert (str(q.dimension) == 'energy')
            assert (q.dtype == float)
            assert (q.unitstr == str(respy.units.Units.energy[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(respy.units.Units.energy[item]))


ops = {'+': operator.add,
       '-': operator.sub,
       '*': operator.mul,
       '/': operator.truediv}

unit = [units.m, 1 / units.m, units.m ** 2, 1 / units.m ** 2]

a, b, c, d, a_unit, b_unit, c_unit, d_unit = (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
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
