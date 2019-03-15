# -*- coding: utf-8 -*-
"""
Dimension of Physical Quantities
--------------------------------
Created on 28.01.2019 by Ismail Baris

This module contains the dimensions for the units.
"""
from __future__ import division
from sympy.physics.units.dimensions import (Dimension, frequency, length, energy, power,
                                            temperature, volume, time, mass, current)

area = Dimension(name='area', symbol='A')
volume = volume
frequency = frequency
length = length
energy = energy
power = power
temperature = temperature
time = time
mass = mass
current = current