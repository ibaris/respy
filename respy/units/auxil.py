# -*- coding: utf-8 -*-
"""
Created on 26.01.2019 by Ismail Baris
"""
from __future__ import division

import operator as op

from respy.units.util import Zero, One

__NONE_UNITS__ = [Zero, One, None]

__ADD_SUB__ = [b'+', b'-']

__BITWISE__ = [b'&', b'^', b'|', b'<<', b'>>']


__UFUNC_NAME__ = {'__add__': '+',
                  '__truediv__': '/',
                  '__rtruediv__': '/',
                  '__floordiv__': '//',
                  '__rfloordiv__': '//',
                  '__and__': '&',
                  '__rand__': '&',
                  '__xor__': '^',
                  '__rxor__': '^',
                  '__or__': '|',
                  '__ror__': '|',
                  '__pow__': '**',
                  '__rpow__': '**',
                  '__lshift__': '<<',
                  '__rlshift__': '<<',
                  '__mul__': '*',
                  '__rshift__': '>>',
                  '__rrshift__': '>>',
                  '__sub__': '-',
                  '__rsub__': '-',
                  '__lt__': '<',
                  '__le__': '<=',
                  '__eq__': '==',
                  '__ne__': '!=',
                  '__ge__': '>=',
                  '__gt__': '>',
                  '__mod__': '%',
                  '__rmod__': '%',
                  '__abs__': 'abs',
                  '__pos__': 'pos',
                  '__neg__': 'neg',
                  '__invert__': '~'}

__OPERATORS__ = {'+': op.add,
                 '/': op.truediv,
                 '//': op.floordiv,
                 '&': op.and_,
                 '^': op.xor,
                 '~': op.invert,
                 '|': op.or_,
                 '**': op.pow,
                 '<<': op.lshift,
                 '*': op.mul,
                 '>>': op.rshift,
                 '-': op.sub,
                 '<': op.lt,
                 '<=': op.le,
                 '==': op.eq,
                 '!=': op.ne,
                 '>=': op.ge,
                 '>': op.gt,
                 '%': op.mod,
                 'abs': op.abs,
                 'pos': op.pos,
                 'neg': op.neg}
