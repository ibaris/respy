# -*- coding: utf-8 -*-
"""
Created on 27.01.2019 by Ismail Baris
"""
from __future__ import division
from cpython cimport bool

cdef tuple check_units(object, object, char*)
cdef char*check_names(char*, char*, bool, bool)
