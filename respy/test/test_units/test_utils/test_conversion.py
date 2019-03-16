# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from __future__ import division
import respy as rpy
from respy.bin_units.wrapper import convert_to_unit
from sympy.physics.units import convert_to
import numpy as np
import pytest
n = 10

@pytest.mark.webtest
@pytest.mark.parametrize("unit",
                         [(rpy.Units.temperature.values()),
                          (rpy.Units.power.values()),
                          (rpy.Units.energy.values()),
                          (rpy.Units.current.values()),
                          (rpy.Units.length.values()),
                          (rpy.Units.frequency.values()),
                          (rpy.Units.mass.values()),
                          (rpy.Units.other.values()),
                          (rpy.Units.time.values())])
class TestConversion:
    def test_random_arrays_with_units(self, unit):

        for x in range(n):
            expr_unit = np.random.choice(unit)
            convert_unit = np.random.choice(unit)

            expr = np.random.random(10) * expr_unit

            convert_respy = convert_to_unit(expr, convert_unit)

            convert_sympy = np.zeros_like(convert_respy)
            for i in range(expr.shape[0]):
                arg = convert_to(expr[i], convert_unit).n()
                convert_sympy[i] = arg.args[0]

            assert np.allclose(convert_respy, convert_sympy)
