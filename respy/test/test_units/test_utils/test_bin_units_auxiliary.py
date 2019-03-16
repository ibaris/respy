# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from __future__ import division

import numpy as np
from sympy import zoo, oo, S

from respy import Units
from respy.bin_units.wrapper import unit_isnone, dim_isnone

n = 100

__NONE_UNITS__ = [S.Zero, S.One, None, zoo, oo, S.NaN]


class TestNoneUnitsAndDimensions:
    def test_none_unit(self):
        units = Units.units.values()

        for item in units:
            assert (not unit_isnone(item))

        for x in range(n):
            assert (unit_isnone(np.random.choice(__NONE_UNITS__)))

    def test_none_dim(self):
        units = [Units.angle.values(), Units.area.values(), Units.current.values(), Units.energy.values(),
                 Units.frequency.values(), Units.length.values(), Units.mass.values(), Units.power.values(),
                 Units.temperature.values(), Units.time.values()]

        for i in range(len(units)):
            items = units[i]

            for item in items:
                assert (not dim_isnone(item))

        for x in range(n):
            assert (dim_isnone(np.random.choice(__NONE_UNITS__)))
