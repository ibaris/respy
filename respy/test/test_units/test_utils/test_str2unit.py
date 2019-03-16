# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from __future__ import division

import operator

import numpy as np

from respy import Units
from respy.bin_units.wrapper import get_unitstr, unit_isnone

n = 300

__OPERAND_STR__ = ['*', '/', '+', '-', '**']
__OPERAND__ = [operator.mul, operator.div, operator.add, operator.sub, operator.pow]

__OPERATOR__ = dict(zip(__OPERAND_STR__, __OPERAND__))


class Test2UnitAnd2String:
    def test_2unit(self):
        unit_str = Units.units.keys()

        for x in range(n):
            operator_str = np.random.choice(__OPERATOR__.keys())
            operand = __OPERATOR__[operator_str]

            i, j = np.random.randint(0, len(unit_str)), np.random.randint(0, len(unit_str))
            expr = unit_str[i] + ' ' + operator_str + ' ' + unit_str[j]
            unit_expr = operand(Units.units[unit_str[i]], Units.units[unit_str[j]])

            str2unit = get_unitstr(expr)

            assert (str2unit == unit_expr)

    def test_2string(self):
        unit_str = Units.units.keys()

        for x in range(n):
            operator_str = np.random.choice(__OPERATOR__.keys())
            operand = __OPERATOR__[operator_str]

            i, j = np.random.randint(0, len(unit_str)), np.random.randint(0, len(unit_str))
            expr = unit_str[i] + ' ' + operator_str + ' ' + unit_str[j]
            unit_expr = operand(Units.units[unit_str[i]], Units.units[unit_str[j]])

            str2unit = get_unitstr(expr)

            unit2str = Units.unit2str(str2unit)

            try:
                assert (unit2str == str(unit_expr))
            except AssertionError:
                if unit2str == b'' and unit_isnone(unit_expr):
                    pass
                else:
                    raise AssertionError