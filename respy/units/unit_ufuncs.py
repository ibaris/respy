# -*- coding: utf-8 -*-
"""
Created on 04.02.2019 by Ismail Baris
"""
from __future__ import division
import sympy as sym
import operator

# class UfuncHelpers(dict):
#     """Registry of unit conversion functions to help ufunc evaluation.
#
#     Based on dict for quick access, but with a missing method to load
#     helpers for additional modules such as scipy.special and erfa.
#
#     Such modules should be registered using ``register_module``.
#     """
#     UNSUPPORTED = set()
#
#
#     def register_module(self, module, names, importer):
#         """Register (but do not import) a set of ufunc helpers.
#
#         Parameters
#         ----------
#         module : str
#             Name of the module with the ufuncs (e.g., 'scipy.special').
#         names : iterable of str
#             Names of the module ufuncs for which helpers are available.
#         importer : callable
#             Function that imports the ufuncs and returns a dict of helpers
#             keyed by those ufuncs.  If the value is `None`, the ufunc is
#             explicitly *not* supported.
#         """
#         self.modules[module] = {'names': names,
#                                 'importer': importer}
#
#     @property
#     def modules(self):
#         """Modules for which helpers are available (but not yet loaded)."""
#         if not hasattr(self, '_modules'):
#             self._modules = {}
#
#         return self._modules
#
#     @property
#     def register_ufunc_converter(self, numpy_ufunc, sympy_ufunc):
#         pass
#
# u = UfuncHelpers()


__CONVERT__MATH__ = {"power": sym.power,  # Unit must be checked
                     "remainder": operator.div,
                     "sqrt": sym.sqrt,
                     "cbrt": sym.cbrt,
                     "gcd": sym.gcd,  # Unit must be checked
                     "lcm": sym.lcm}  # Unit must be checked

__MATH_UNIT_GETS_LOST__ = ["signbit",
                           "mod",
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
                                "conj",
                                "conjugate",
                                "nan_to_num"]

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

__NOT_IMPLEMENTED__ = ["copysign",
                       "nextafter",
                       "spacing",
                       "modf",
                       "ldexp",
                       "frexp",
                       "fmod",
                       "floor",
                       "ceil",
                       "trunc"]
