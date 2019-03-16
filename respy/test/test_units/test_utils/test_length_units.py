# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from respy.units.unit import __unit__, __values__

class TestLength:
    def test_length(self):
        assert(len(__unit__) == len(__values__))