# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from __future__ import division
from respy.units import Quantity
from respy.units import dimensions
from respy.units import util
from respy import constants as const
import numpy as np

T4 = Quantity(4000, 'K')
T5 = Quantity(5000, 'K')
T6 = Quantity(6000, 'K')
T7 = Quantity(7000, 'K')
wavelengths = np.arange(1000.0 * 1e-10, 20000. * 1e-10, 20e-10)

input = Quantity(wavelengths, 'm')


def planck(Tempreture, input, unit='GHz'):
    if hasattr(Tempreture, 'quantity'):
        if Tempreture.dimension == dimensions.temperature:
            Tempreture = Tempreture.convert_to('K')
        else:
            raise ValueError("{0} is not a valid dimension for temperature.".format(Tempreture.dimension))

    if hasattr(input, 'quantity'):
        if input.dimension == dimensions.length:
            if input.unit is util.m:
                pass
            else:
                input = input.convert_to('m')

            numerator = 2. * np.pi * const.h * (const.c ** 2) / (input ** 5)
            b = const.h * const.c / (input * const.k_b * Tempreture)
            result = numerator / np.expm1(b)
            result = Quantity(result, unit=util.watt / (util.m ** 2 * util.m))

        elif input.dimension == dimensions.frequency:
            pass

    return result


intensity4000 = planck(T7, input)
# intensity5000 = planck(T5, input)
# intensity6000 = planck(T6, input)
# intensity7000 = planck(T7, input)

import matplotlib.pyplot as plt

plt.hold(True)  # doesn't erase plots on subsequent calls of plt.plot()
plt.plot(wavelengths * 1e9, intensity4000, 'r-')
# plot intensity4000 versus wavelength in nm as a red line
# plt.plot(wavelengths*1e9, intensity5000.value, 'g-') # 5000K green line
# plt.plot(wavelengths*1e9, intensity6000.value, 'b-') # 6000K blue line
# plt.plot(wavelengths*1e9, intensity7000.value, 'k-') # 7000K black line

# show the plot
plt.show()
