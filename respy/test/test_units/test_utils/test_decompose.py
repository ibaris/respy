# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from __future__ import division
import operator
from respy import decompose, Units
import numpy as np
import pytest

n = 300

__OPERAND_STR__ = ['*', '/']
__OPERAND__ = [operator.mul, operator.div]

__OPERATOR__ = dict(zip(__OPERAND_STR__, __OPERAND__))


class TestDecompose:
    def test_expr(self):
        unit_str = Units.units.keys()

        for x in range(n):
            operator_str = np.random.choice(__OPERATOR__.keys())
            operand = __OPERATOR__[operator_str]

            random_number = np.random.random()

            i = np.random.randint(0, len(unit_str))

            unit_expr = operand(random_number, Units.units[unit_str[i]])

            manual_decompose = (random_number, operand(1, Units.units[unit_str[i]]))

            decomposed = decompose(unit_expr)

            assert (manual_decompose == decomposed)

    def test_array(self):
        unit_str = Units.units.keys()

        for x in range(n):
            operator_str = np.random.choice(__OPERATOR__.keys())
            operand = __OPERATOR__[operator_str]

            random_number = np.random.random(5)

            i = np.random.randint(0, len(unit_str))

            unit_expr = operand(random_number, Units.units[unit_str[i]])

            manual_decompose = (random_number, operand(1, Units.units[unit_str[i]]))

            decomposed = decompose(unit_expr)

            assert (np.all(manual_decompose[0] == decomposed[0]))
            assert(manual_decompose[1] == decomposed[1])

    def test_valueerror(self):
        unit_str = Units.units.keys()

        for x in range(n):
            operator_str = np.random.choice(__OPERATOR__.keys())
            operand = __OPERATOR__[operator_str]

            random_number = np.random.random(5)

            i, j = 0, 0
            while Units.units[unit_str[i]] == Units.units[unit_str[j]]:
                i, j = np.random.randint(0, len(unit_str)), np.random.randint(0, len(unit_str))

            unit_expr = operand(random_number, Units.units[unit_str[i]])
            unit_expr[0:2] = operand(random_number[0:2], Units.units[unit_str[j]])

            with pytest.raises(ValueError):
                decompose(unit_expr)

    def test_typeerror(self):
        item_list = ['string', [], (), {}]

        for item in item_list:
            with pytest.raises(TypeError):
                decompose(item)