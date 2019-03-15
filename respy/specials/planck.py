# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from __future__ import division
from respy.units import Quantity, util, dimensions, UnitError, DimensionError, Units
from respy import constants as const
import numpy as np


def planck(temperature, input, temperature_unit='K', input_unit='Hz'):
    if hasattr(temperature, 'quantity'):
        pass
    elif temperature_unit in Units.temperature.keys() or temperature_unit in Units.temperature.values():
        temperature = Quantity(temperature, temperature_unit)

    if temperature.dimension == dimensions.temperature:
        if input.unit is util.K:
            pass
        else:
            temperature = temperature.convert_to('K')
    else:
        raise DimensionError("{0} is not a valid dimension for temperature.".format(temperature.dimension))

    if hasattr(input, 'quantity'):
        pass
    elif (input_unit in Units.frequency.keys() or input_unit in Units.frequency.values() or
          input_unit in Units.length.keys() or input_unit in Units.length.values()):

        input = Quantity(input, input_unit)

    else:
        raise UnitError("{0} is not a valid unit for frequency or wavelength.".format(str(input_unit)))

    if input.dimension == dimensions.length:
        if input.unit is util.m:
            pass
        else:
            input = input.convert_to('m')

        numerator = 2. * const.pi * const.h * (const.c ** 2) / (input ** 5)
        b = const.h * const.c / (input * const.k_b * temperature)
        result = numerator / np.expm1(b)
        result = Quantity(result, unit=util.watt / (util.m ** 2 * util.m))

    elif input.dimension == dimensions.frequency:
        if input.unit is util.hz:
            pass
        else:
            input = input.convert_to('Hz')

        numerator = 2 * const.pi * const.h * (input ** 3) / (const.c ** 2)
        b = const.h * input / (const.k_b * temperature)
        result = numerator / np.expm1(b)
        result = Quantity(result, unit=util.watt / (util.m ** 2 * util.Hz))

    else:
        raise DimensionError("{0} is not a valid dimension for frequency or wavelength.".format(input.dimension))

    return result
