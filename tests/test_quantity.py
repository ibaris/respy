from __future__ import division
import respy as rsp
import numpy as np


class TestInput:
    def test_input_plain(self):
        value = 23
        unit = 'GHz'
        name = 'Test Case'
        q = rsp.units.Quantity(value=value, unit=unit, name=name)

        assert (q.name == name)
        assert (str(q.dimension) == 'frequency')
        assert (q.dtype == float)
        assert (q.unitstr == str(rsp.Units.frequency[unit]))
        assert (q.value == value)
        assert (repr(q) == '<Quantity [23.] Test Case in [gigahertz]>')

    def test_input_sympy(self):
        value = 23 * rsp.Units.frequency.GHz
        # unit = 'GHz'
        name = 'Test Case Units'
        q = rsp.units.Quantity(value=value, name=name, subok=True)

        assert (q.name == name)
        assert (str(q.dimension) == 'frequency')
        assert (q.dtype == float)
        assert (q.unit == rsp.Units.frequency.GHz)
        assert (q.value == 23)
        assert (repr(q) == '<Quantity [23.] Test Case Units in [gigahertz]>')

    def test_input_none(self):
        value = 23
        name = 'Test Case'
        q = rsp.units.Quantity(value=value, name='Test Case')

        assert (q.name == name)
        assert (str(q.dimension) == 'None')
        assert (q.dtype == float)
        assert (q.unitstr == '-')
        assert (q.value == value)
        assert (repr(q) == '<Quantity [23.] Test Case in [-]>')

    def test_input_no_name(self):
        value = 23
        unit = 'GHz'
        q = rsp.units.Quantity(value=value, unit=unit)

        assert (q.name is None)
        assert (str(q.dimension) == 'frequency')
        assert (q.dtype == float)
        assert (q.unitstr == str(rsp.Units.frequency[unit]))
        assert (q.value == value)
        assert (repr(q) == '<Quantity [23.] [gigahertz]>')

    def test_input_all_array(self):

        value = np.linspace(1, 100, 10)
        unit = 'meter'
        name = 'Test Case Array'
        q = rsp.units.Quantity(value=value, unit=unit, name=name)

        assert (q.name == name)
        assert (str(q.dimension) == 'length')
        assert (q.dtype == float)
        assert (q.unitstr == str(rsp.Units.length[unit]))
        assert (np.all(q.value == value))
        assert (repr(
            q) == '<Quantity [  1.,  12.,  23.,  34.,  45.,  56.,  67.,  78.,  89., 100.] Test Case Array in [meter]>')

    def test_input_dimension(self):
        value = np.linspace(0, 20, 5)

        for item in rsp.Units.frequency.keys():
            unit = item
            q = rsp.units.Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (str(q.dimension) == 'frequency')
            assert (q.dtype == float)
            assert (q.unitstr == str(rsp.Units.frequency[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(rsp.Units.frequency[item]))

        for item in rsp.Units.length.keys():
            unit = item
            q = rsp.units.Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (str(q.dimension) == 'length')
            assert (q.dtype == float)
            assert (q.unitstr == str(rsp.Units.length[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(rsp.Units.length[item]))

        for item in rsp.Units.other.keys():
            unit = item
            q = rsp.units.Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (str(q.dimension) == 'None')
            assert (q.dtype == float)
            assert (q.unitstr == str(rsp.Units.other[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(rsp.Units.other[item]))

        for item in rsp.Units.temperature.keys():
            unit = item
            q = rsp.units.Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (str(q.dimension) == 'temperature')
            assert (q.dtype == float)
            assert (q.unitstr == str(rsp.Units.temperature[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(rsp.Units.temperature[item]))

        for item in rsp.Units.time.keys():
            unit = item
            q = rsp.units.Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (str(q.dimension) == 'time')
            assert (q.dtype == float)
            assert (q.unitstr == str(rsp.Units.time[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(rsp.Units.time[item]))

        for item in rsp.Units.energy.keys():
            unit = item
            q = rsp.units.Quantity(value=value, unit=unit)
            assert (q.name is None)
            assert (str(q.dimension) == 'energy')
            assert (q.dtype == float)
            assert (q.unitstr == str(rsp.Units.energy[item]))
            assert (np.all(q.value == value))
            assert (repr(q) == '<Quantity [ 0.,  5., 10., 15., 20.] [{}]>'.format(rsp.Units.energy[item]))
