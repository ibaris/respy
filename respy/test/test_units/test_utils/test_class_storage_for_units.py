# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from __future__ import division
import numpy as np
import pytest
from respy.units.util import (Frequency, Length, Energy, Power, Time, Temperature, Mass, Current, Other, Area, Volume,
                              Angle)

dicts = [Frequency, Length, Energy, Power, Time, Temperature, Mass, Current, Other, Area, Volume,
         Angle]


class TestAll:
    def test_dicts(self):
        for item in dicts:
            a = np.random.random()

            a_item = item(a=a)

            assert a_item.a == a

    def test_dicts_err(self):
        for item in dicts:
            a = np.random.random()

            a_item = item(a=a)

            with pytest.raises(AttributeError):
                a_item.b

    def test_dicts_dir(self):
        for item in dicts:
            a = np.random.random()

            a_item = item(a=a)

            assert dir(a_item) == ['a']

    def test_repr(self):
        for item in dicts:
            a = round(np.random.random(), 2)

            a_item = item(a=a)

            assert repr(a_item) == ' a: ' + str(a)