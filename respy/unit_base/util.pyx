# -*- coding: utf-8 -*-
"""
Utility of Physical Quantities
------------------------------
Created on 27.01.2019 by Ismail Baris

This Module contains utility functions like the check of units and names.
"""
from __future__ import division
from cpython cimport bool

cdef char*check_names(char*name1, char*name2, bool constant1, bool constant2):
    """
    Check and select the right name.
    
    Parameters
    ----------
    name1 : char*
        First name.
    name2 : char*
        Second name.
    constant1 : bool
        Choose if the first name is defined as constant. 
    constant2 : bool
        Choose if the second name is defined as constant. 

    Returns
    -------
    char*
    
    """

    if name1 == b'' and name2 == b'':
        name = b''
    elif name1 == b'' and name2 != b'':
        name = name2 if not constant1 else b''
    elif name1 != b'' and name2 == b'':
        name = name1 if not constant1 else b''
    else:
        name = b''

    return name
