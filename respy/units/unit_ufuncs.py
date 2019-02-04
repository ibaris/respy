# -*- coding: utf-8 -*-
"""
Created on 04.02.2019 by Ismail Baris
"""
from __future__ import division
import sympy as sym
import operator

__CONVERT__MATH__ = {"power": sym.power,  # Unit must be checked
                     "remainder": operator.div,
                     "sqrt": sym.sqrt,
                     "cbrt": sym.cbrt,
                     "gcd": sym.gcd,  # Unit must be checked
                     "lcm": sym.lcm}  # Unit must be checked

__MATH_UNIT_GETS_LOST__ = ["mod",
                           "fmod",
                           "divmod",
                           "logaddexp",
                           "logaddexp2",
                           "sign",
                           "heaviside",
                           "exp",
                           "exp2",
                           "log",
                           "log2",
                           "log10",
                           "expm1",
                           "log1p",
                           "sin",
                           "cos",
                           "tan",
                           "arcsin",
                           "arccos",
                           "arctan",
                           "arctan2",
                           "hypot",
                           "sinh",
                           "cosh",
                           "tanh",
                           "arcsinh",
                           "arccosh",
                           "arctanh",
                           "deg2rad",
                           "rad2deg",
                           "bitwise_and",
                           "bitwise_or",
                           "bitwise_xor",
                           "invert",
                           "left_shift",
                           "right_shift"]

__MATH_UNIT_REMAINS_STABLE__ = ["absolute",
                                "fabs",
                                "negative",
                                "positive",
                                "rint",
                                "conj"]

__CHECK_UNIT__ = ["power",  # Unit must be checked
                  "gcd",  # Unit must be checked
                  "lcm"]  # Unit must be checked

__MATH_LOGICAL_AND_MORE__ = ["greater",
                             "greater_equal",
                             "less",
                             "less_equal",
                             "not_equal",
                             "equal",
                             "logical_and",
                             "logical_or",
                             "logical_xor",
                             "logical_not",
                             "isfinite",
                             "isinf",
                             "isnan",
                             "isnat"]

__NOT_IMPLEMENTED__ = ["signbit",
                       "copysign",
                       "nextafter",
                       "spacing",
                       "modf",
                       "ldexp",
                       "frexp",
                       "fmod",
                       "floor",
                       "ceil",
                       "trunc"]
