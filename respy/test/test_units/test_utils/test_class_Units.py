# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from __future__ import division
from respy import Units, unit_isnone
from respy.units.auxil import __OPERAND__, One, Zero
from respy.errors import UnitError
import operator
import numpy as np
import pytest

n = 300

__OPERAND_OBJECT__ = [operator.mul, operator.div, operator.add, operator.sub, operator.pow]

__OPERATOR__ = dict(zip(__OPERAND__, __OPERAND_OBJECT__))


class TestAttributes:
    def test_dim(self):
        assert (len(Units.dimensions) == len(Units.__unit_dict__) - 1)

    def test_len_setup(self):
        lens = 0

        for item in Units:
            lens += len(item)

        lens -= len(Units.dimensions)  # Unit class has 11 dimensions, which contributes to length.

        assert (len(Units.units))


dir_list = ['_Units__unit_dict',
            'angle',
            'area',
            'current',
            'dimensions',
            'energy',
            'frequency',
            'length',
            'mass',
            'other',
            'power',
            'temperature',
            'time',
            'units',
            'volume']


class TestDictMethods:
    def test_dicts(self):

        assert dir(Units) == dir_list

    def test_dicts_err(self):
        keys = ['a', 'b', 'c']
        for item in keys:
            with pytest.raises(AttributeError):
                Units.item

    def test_links_to_dimensions(self):
        for i in range(1, len(dir_list)):
            item = dir_list[i]

            if item in ['dimensions', 'units']:
                pass
            else:
                assert item in str(Units[item].__class__).lower()


class TestMethodsConversion:
    def test_2unit(self):
        unit_str = Units.units.keys()

        for x in range(n):
            operator_str = np.random.choice(__OPERATOR__.keys())
            operand = __OPERATOR__[operator_str]

            i, j = np.random.randint(0, len(unit_str)), np.random.randint(0, len(unit_str))
            expr = unit_str[i] + ' ' + operator_str + ' ' + unit_str[j]
            unit_expr = operand(Units.units[unit_str[i]], Units.units[unit_str[j]])

            str2unit = Units.str2unit(expr)

            assert (str2unit == unit_expr)

    def test_2string(self):
        unit_str = Units.units.keys()

        for x in range(n):
            operator_str = np.random.choice(__OPERATOR__.keys())
            operand = __OPERATOR__[operator_str]

            i, j = np.random.randint(0, len(unit_str)), np.random.randint(0, len(unit_str))
            expr = unit_str[i] + ' ' + operator_str + ' ' + unit_str[j]
            unit_expr = operand(Units.units[unit_str[i]], Units.units[unit_str[j]])

            str2unit = Units.str2unit(expr)

            unit2str = Units.unit2str(str2unit)

            try:
                assert (unit2str == str(unit_expr))
            except AssertionError:
                if unit2str == b'' and unit_isnone(unit_expr):
                    pass
                else:
                    raise AssertionError

    def test_get_unit(self):
        unit_str = Units.units.keys()

        for x in range(n):
            operator_str = np.random.choice(__OPERATOR__.keys())
            operand = __OPERATOR__[operator_str]

            i, j = np.random.randint(0, len(unit_str)), np.random.randint(0, len(unit_str))
            expr = unit_str[i] + ' ' + operator_str + ' ' + unit_str[j]
            unit_expr = operand(Units.units[unit_str[i]], Units.units[unit_str[j]])

            str2unit = Units.get_unit(expr)

            assert (str2unit == unit_expr)

    def test_get_unit_expr(self):
        unit_str = Units.units.keys()

        for x in range(n):
            operator_str = np.random.choice(__OPERATOR__.keys())
            operand = __OPERATOR__[operator_str]

            i, j = np.random.randint(0, len(unit_str)), np.random.randint(0, len(unit_str))
            unit_expr = operand(Units.units[unit_str[i]], Units.units[unit_str[j]])

            str2unit = Units.get_unit(unit_expr)

            assert (str2unit == unit_expr)

    def test_get_unit_error(self):
        items = ['a', '1/m', 'mk*334kdj', 'skjf']

        for item in items:
            with pytest.raises(UnitError):
                Units.get_unit(item)

    def test_error_2unit(self):
        items = ['a', '1/m', 'mk*334kdj', 'skjf']

        for item in items:
            with pytest.raises(UnitError):
                Units.str2unit(item)

    def test_attr_error(self):
        items = ['a', '1/m', 'mk*334kdj', 'skjf']

        for item in items:
            with pytest.raises(KeyError):
                Units[item]


class TestMethods:
    def test_get_dim_all(self):
        unit_str = Units.units.keys()

        for item in unit_str:
            unit = Units.units[item]
            dim = Units.get_dim(unit)

            assert (unit.dimension == dim)

    def test_get_dim_area(self):
        unit_str = Units.length.keys()

        for item in unit_str:
            unit = Units.units[item] ** 2
            dim = Units.get_dim(unit)

            assert (Units.dimensions['area'] == dim)

    def test_get_dim_volume(self):
        unit_str = Units.length.keys()

        for item in unit_str:
            unit = Units.units[item] ** 3
            dim = Units.get_dim(unit)

            assert (Units.dimensions['volume'] == dim)

    def test_get_dim_ones(self):
        unit_str = Units.length.keys()

        for item in unit_str:
            unit = Units.units[item] ** 4
            dim = Units.get_dim(unit)

            assert (One == dim)

    def test_get_dim_zeros(self):
        items = ['1 / GHz ** 2', '1 / m', '1 / nm ** 3']

        for item in items:
            dim = Units.get_dim(item)

            assert (Zero == dim)

    def test_dim_isone(self):
        unit_str = Units.length.keys()

        for item in unit_str:
            unit = Units.units[item] ** 4
            dim = Units.dim_isnone(unit)

            assert dim

    def test_dim_iszero(self):
        items = ['1 / GHz ** 2', '1 / m', '1 / nm ** 3']

        for item in items:
            dim = Units.dim_iszero(item)

            assert dim
