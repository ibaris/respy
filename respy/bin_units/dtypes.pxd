# -*- coding: utf-8 -*-
# cython: cdivision=True
"""
Created on 15.03.2019 by Ismail Baris
"""
import numpy as np
cimport numpy as np

ctypedef fused DTYPE_ARRAY:
    np.ndarray
    int[:]
    double[:]
    long long[:]
    float[:]
    int[:,:]
    double[:,:]
    long long[:,:]
    float[:,:]
    int[:,:,:]
    double[:,:,:]
    long long[:,:,:]
    float[:,:,:]
    complex[:]
    complex[:,:]
    complex[:,:,:]


ctypedef fused DTYPE_SCALAR:
    int
    double
    long long
    float
