# -*- coding: utf-8 -*-
"""
Created on 26.01.2019 by Ismail Baris
"""
from __future__ import division

import operator as op
import sympy as sym
from respy.units.unit import __unit__, __values__

__OPERAND__ = ['*', '/', '+', '-', '**']

__UNITS__ = dict(zip(__unit__, __values__))
__SYMPY_CLASSES__ = tuple(sym.core.all_classes)
__NONE_UNIT_TYPES__ = [sym.S.Zero, sym.S.One, None, sym.zoo, sym.oo, sym.S.NaN]
__NONE_DIM_TYPES__ = [None, sym.zoo, sym.oo, sym.S.NaN]
Zero = sym.S.Zero
One = sym.S.One
zoo = sym.zoo
oo = sym.oo
NaN = sym.S.NaN

__NONE_UNITS__ = __NONE_UNIT_TYPES__

__SAME_UNIT_OPERATOR__ = [op.add.__name__, op.sub.__name__, op.and_.__name__, op.xor.__name__,
                          op.or_.__name__, op.lshift.__name__, op.rshift.__name__, op.mod.__name__]

__POW__ = [b'**']

__OPERATOR__ = {'__add__': op.add,
                '__truediv__': op.truediv,
                '__rtruediv__': op.truediv,
                '__floordiv__': op.floordiv,
                '__rfloordiv__': op.floordiv,
                '__and__': op.and_,
                '__rand__': op.and_,
                '__xor__': op.xor,
                '__rxor__': op.xor,
                '__or__': op.or_,
                '__ror__': op.or_,
                '__pow__': op.pow,
                '__rpow__': op.pow,
                '__lshift__': op.lshift,
                '__rlshift__': op.lshift,
                '__mul__': op.mul,
                '__rshift__': op.rshift,
                '__rrshift__': op.rshift,
                '__sub__': op.sub,
                '__rsub__': op.sub,
                '__lt__': op.lt,
                '__le__': op.le,
                '__eq__': op.eq,
                '__ne__': op.ne,
                '__ge__': op.ge,
                '__gt__': op.gt,
                '__mod__': op.mod,
                '__rmod__': op.mod,
                '__abs__': op.abs,
                '__pos__': op.pos,
                '__neg__': op.neg,
                '__invert__': op.invert}
