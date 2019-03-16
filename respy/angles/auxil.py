# -*- coding: utf-8 -*-
"""
Created on  by Ismail Baris
"""
from respy.util import (asarrays, valid_dtype)
import numpy as np

__ANGLE_UNIT_RAD__ = ['RAD', 'rad', 'radian', 'radians']
__ANGLE_UNIT_DEG__ = ['DEG', 'deg', 'degree', 'degrees']


def unit_is_rad(unit):
    if unit in __ANGLE_UNIT_RAD__:
        return True

    return False


def unit_is_deg(unit):
    if unit in __ANGLE_UNIT_DEG__:
        return True

    return False


def check_angles(iza, vza, raa, iaa, vaa, alpha, beta, angle_unit, dtype):
    if raa is None and (iaa is None or vaa is None):
        raise ValueError("If raa is not defined iaa AND vaa must be defined.")

    if unit_is_rad(angle_unit) or unit_is_deg(angle_unit):
        pass
    else:
        raise ValueError("angle_unit must be {0} or {1}, "
                         "but the actual angle_unit is: {2}".format(str(__ANGLE_UNIT_RAD__),
                                                                    str(__ANGLE_UNIT_DEG__),
                                                                    str(angle_unit)))

    if valid_dtype(dtype):
        pass
    else:
        raise TypeError("dtype must be a numpy.dtype object. The actual dtype is {0}".format(str(dtype)))

    # Assign relative azimuth angle flag
    if raa is not None and iaa is not None and vaa is not None:
        raise AssertionError("The relative, incidence and viewing azimuth angle is defined. "
                             "Either raa or iaa AND vaa must be defined. ")
    if raa is None:
        raa_flag = False
        iaa = iaa
        vaa = vaa
        raa = iaa - vaa

    else:
        raa_flag = True
        raa = raa
        iaa = np.zeros_like(raa)
        vaa = np.zeros_like(raa)

    iza, vza, raa, iaa, vaa, alpha, beta = asarrays((iza, vza, raa, iaa, vaa, alpha, beta), dtype=dtype)

    return iza, vza, raa, iaa, vaa, alpha, beta, raa_flag
