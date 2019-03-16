# -*- coding: utf-8 -*-
"""
Physical Constants
------------------
Created on 15.01.2019 by Ismail Baris

This module defines some remote sensing related constants as `Quantity` object.
"""

from __future__ import division
from respy.units import Quantity
from respy.units import unit
import sympy

system = 'SI'

k_B = k_b = Quantity(1.38064852e-23, name="Boltzmann constant", unit="joule / kelvin", constant=True)
c = Quantity(299792458.0, name="Speed of light in vacuum", unit="meter / second", constant=True)
h = Quantity(6.62606957e-34, name="Planck constant", unit="joule * second", constant=True)
u0 = Quantity(1.25663706143592e-6, unit=unit.kilogram * unit.meter / (unit.ampere ** 2 * unit.second ** 2),
              name="Magnetic Constant", constant=True)
e0 = Quantity(8.85418781762039e-12, unit=unit.ampere ** 2 * unit.second ** 4 / (unit.kilogram * unit.meter ** 3),
              name="Electric Constant", constant=True)

pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164
rad_to_deg = 180.0 / pi
deg_to_rad = pi / 180.0
#
# __CONSTANTS__ = [k_B, c, h, u0, e0]
#
#
# def summary():
#     header = "Available Constants\n-------------------\n"
#     body = __CONSTANTS__[0].name + '. Abbrev: ' + 'k_B.' + ' unit: ' + __CONSTANTS__[0].unitstr + '\n' \
#            + __CONSTANTS__[1].name + '. Abbrev: ' + 'c.' + ' unit: ' + __CONSTANTS__[1].unitstr + '\n' \
#            + __CONSTANTS__[2].name + '. Abbrev: ' + 'h.' + ' unit: ' + __CONSTANTS__[2].unitstr + '\n' \
#            + __CONSTANTS__[3].name + '. Abbrev: ' + 'u0.' + ' unit: ' + __CONSTANTS__[3].unitstr + '\n' \
#            + __CONSTANTS__[4].name + '. Abbrev: ' + 'e0.' + ' unit: ' + __CONSTANTS__[4].unitstr + '\n'
#
#     other = "Other constants are pi, rad_to_deg and deg_to_rad"
#     print (header + body + other)
