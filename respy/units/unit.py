# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from __future__ import division

import sympy.physics.units as sympy_units
from sympy import S
from sympy.physics.units.quantities import Quantity as sQuantity

from respy.units import dimensions

__all__ = ['deg', 'degree', 'degrees', 'rad', 'radian', 'radians', 'decibel', 'dB', 'millihertz', 'mhz', 'mHz',
           'centihertz', 'chz', 'cHz', 'decihertz', 'dhz', 'dHz', 'hertz', 'hz', 'Hz', 'decahertz', 'dahz', 'daHz',
           'hectohertz', 'hhz', 'hHz', 'kilohertz', 'khz', 'kHz', 'megahertz', 'MHz', 'gigahertz', 'ghz', 'GHz',
           'terahertz', 'thz', 'THz', 'petahertz', 'phz', 'PHz', 'nm', 'nanometers', 'nanometer', 'um', 'micrometers',
           'micrometer', 'mm', 'millimeters', 'millimeter', 'cm', 'centimeters', 'centimeter', 'dm', 'decimeters',
           'decimeter', 'm', 'meters', 'meter', 'km', 'kilometers', 'kilometer', 's', 'second', 'seconds', 'minute',
           'minutes', 'h', 'hour', 'hours', 'K', 'kelvins', 'kelvin', 'J', 'joules', 'joule', 'W', 'watt',
           'watts', 'milligram', 'milligrams', 'mg', 'microgram', 'micrograms', 'ug', 'gram', 'grams', 'g',
           'kilogram', 'kilograms', 'kg', 'ampere', 'amperes', 'A', 'One', 'linear']

One = S.One

deg = degree = degrees = sympy_units.degree
rad = radian = radians = sympy_units.radian

decibel = dB = sQuantity("decibel", abbrev="dB")
dB.set_dimension(One)
dB.set_scale_factor(One)

linear = sQuantity("linear")
linear.set_dimension(One)
linear.set_scale_factor(One)

millihertz = mhz = mHz = sQuantity("millihertz", abbrev="mHz")
millihertz.set_dimension(dimensions.frequency)
millihertz.set_scale_factor(1 / 1e3)

centihertz = chz = cHz = sQuantity("centihertz", abbrev="cHz")
centihertz.set_dimension(dimensions.frequency)
centihertz.set_scale_factor(1 / 1e2)

decihertz = dhz = dHz = sQuantity("decihertz", abbrev="dHz")
decihertz.set_dimension(dimensions.frequency)
decihertz.set_scale_factor(1 / 1e1)

hertz = hz = Hz = sQuantity("hertz", abbrev="Hz")
hertz.set_dimension(dimensions.frequency)
hertz.set_scale_factor(One)

decahertz = dahz = daHz = sQuantity("decahertz", abbrev="daHz")
decahertz.set_dimension(dimensions.frequency)
decahertz.set_scale_factor(10)

hectohertz = hhz = hHz = sQuantity("hectohertz", abbrev="hHz")
hectohertz.set_dimension(dimensions.frequency)
hectohertz.set_scale_factor(100)

kilohertz = khz = kHz = sQuantity("kilohertz", abbrev="kHz")
kilohertz.set_dimension(dimensions.frequency)
kilohertz.set_scale_factor(1000)

megahertz = MHz = sQuantity("megahertz", abbrev="MHz")
megahertz.set_dimension(dimensions.frequency)
megahertz.set_scale_factor(1e6)

gigahertz = ghz = GHz = sQuantity("gigahertz", abbrev="GHz")
gigahertz.set_dimension(dimensions.frequency)
gigahertz.set_scale_factor(1e9)

terahertz = thz = THz = sQuantity("terahertz", abbrev="THz")
terahertz.set_dimension(dimensions.frequency)
terahertz.set_scale_factor(1e12)

petahertz = phz = PHz = sQuantity("petahertz", abbrev="PHz")
petahertz.set_dimension(dimensions.frequency)
petahertz.set_scale_factor(1e15)

nm = nanometers = nanometer = sympy_units.nm
um = micrometers = micrometer = sympy_units.um
mm = millimeters = millimeter = sympy_units.mm
cm = centimeters = centimeter = sympy_units.cm
dm = decimeters = decimeter = sympy_units.dm
m = meters = meter = sympy_units.m
km = kilometers = kilometer = sympy_units.km

s = second = seconds = sympy_units.second
minute = minutes = sympy_units.minute
h = hour = hours = sympy_units.hour

K = kelvins = kelvin = sympy_units.K

J = joules = joule = sympy_units.J

W = watt = watts = sympy_units.watt

milligram = milligrams = mg = sympy_units.milligram
microgram = micrograms = ug = sympy_units.microgram
gram = grams = g = sympy_units.gram
kilogram = kilograms = kg = sympy_units.kilogram

ampere = amperes = A = sympy_units.ampere

__unit__ = ['deg', 'degree', 'degrees', 'rad', 'radian', 'radians', 'decibel', 'dB', 'millihertz', 'mhz', 'mHz',
            'centihertz', 'chz', 'cHz', 'decihertz', 'dhz', 'dHz', 'hertz', 'hz', 'Hz', 'decahertz', 'dahz', 'daHz',
            'hectohertz', 'hhz', 'hHz', 'kilohertz', 'khz', 'kHz', 'megahertz', 'MHz', 'gigahertz', 'ghz', 'GHz',
            'terahertz', 'thz', 'THz', 'petahertz', 'phz', 'PHz', 'nm', 'nanometers', 'nanometer', 'um', 'micrometers',
            'micrometer', 'mm', 'millimeters', 'millimeter', 'cm', 'centimeters', 'centimeter', 'dm', 'decimeters',
            'decimeter', 'm', 'meters', 'meter', 'km', 'kilometers', 'kilometer', 's', 'second', 'seconds', 'minute',
            'minutes', 'h', 'hour', 'hours', 'K', 'kelvins', 'kelvin', 'J', 'joules', 'joule', 'W', 'watt',
            'watts', 'milligram', 'milligrams', 'mg', 'microgram', 'micrograms', 'ug', 'gram', 'grams', 'g',
            'kilogram', 'kilograms', 'kg', 'ampere', 'amperes', 'A', 'linear']

__values__ = [deg, degree, degrees, rad, radian, radians, decibel, dB, millihertz, mhz, mHz,
              centihertz, chz, cHz, decihertz, dhz, dHz, hertz, hz, Hz, decahertz, dahz, daHz,
              hectohertz, hhz, hHz, kilohertz, khz, kHz, megahertz, MHz, gigahertz, ghz, GHz,
              terahertz, thz, THz, petahertz, phz, PHz, nm, nanometers, nanometer, um, micrometers,
              micrometer, mm, millimeters, millimeter, cm, centimeters, centimeter, dm, decimeters,
              decimeter, m, meters, meter, km, kilometers, kilometer, s, second, seconds, minute,
              minutes, h, hour, hours, K, kelvins, kelvin, J, joules, joule, W, watt,
              watts, milligram, milligrams, mg, microgram, micrograms, ug, gram, grams, g,
              kilogram, kilograms, kg, ampere, amperes, A, linear]
