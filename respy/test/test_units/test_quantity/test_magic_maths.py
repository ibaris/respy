# # -*- coding: utf-8 -*-
# """
# Created on 15.03.2019 by Ismail Baris
#
# Magic mathematical methods to be test: mul, truediv, floordiv, add, sub, pow, rsub, rpow,
# """
# from __future__ import division
# import numpy as np
# import pyrism as pyr
# from numpy import allclose, less
# from respy.units import Quantity
# import operator
#
# import pytest
#
# ops = {'+': operator.add,
#        '-': operator.sub,
#        '*': operator.mul,
#        '/': operator.truediv}
#
# unit = [units.m, 1 / units.m, units.m ** 2, 1 / units.m ** 2]
# #
# a, b, c, d, a_unit, b_unit, c_unit, d_unit = (
# np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
# unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
# unit[np.random.randint(0, 3)])
#
#
# @pytest.mark.webtest
# @pytest.mark.parametrize("a, b, c, d, a_unit, b_unit, c_unit, d_unit", [
#     (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
#      unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
#      unit[np.random.randint(0, 3)]),
#     (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
#      unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
#      unit[np.random.randint(0, 3)]),
#     (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
#      unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
#      unit[np.random.randint(0, 3)]),
#     (np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10), np.random.random_sample(10),
#      unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)], unit[np.random.randint(0, 3)],
#      unit[np.random.randint(0, 3)])
# ])
# class TestOperation:
#     def test_operation_unit(self, a, b, c, d, a_unit, b_unit, c_unit, d_unit):
#         test_list = [a, b, c, d]
#         unit_list = [a_unit, b_unit, c_unit, d_unit]
#
#         for i in range(100):
#             op = random.choice(list(ops.keys()))
#
#             item1_value = random.choice(test_list)
#             item2_value = random.choice(test_list)
#
#             unit1 = random.choice(unit_list)
#             unit2 = unit1
#
#             unit1_temp = item1_value * unit1
#             unit2_temp = item2_value * unit2
#
#             item1 = Quantity(item1_value, unit=unit1)
#             item2 = Quantity(item2_value, unit=unit2)
#
#             test = ops.get(op)(item1, item2)
#             ref = ops.get(op)(unit1_temp, unit2_temp)
#
#             assert np.allclose(test.value, ops.get(op)(item1_value, item2_value))
#
#             try:
#                 assert test.unit == ref[0].as_coeff_mul()[1][1]
#             except IndexError:
#                 pass