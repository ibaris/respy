# -*- coding: utf-8 -*-
"""
Created on 26.02.2019 by Ismail Baris
"""
from __future__ import division
from respy import Angles, EM
import numpy as np
from respy.units import Units
from respy.util import align_all


class Sensor(Angles, EM):
    def __init__(self, input, iza, vza, raa=None, iaa=None, vaa=None, normalize=False, nbar=0.0,
                 angle_unit='DEG', align=True, dtype=np.double, unit='GHz', output='cm', identify=False, name=None):

        Angles.__init__(self, iza=iza, vza=vza, raa=raa, iaa=iaa, vaa=vaa, normalize=normalize, nbar=nbar,
                        angle_unit=angle_unit, align=align, dtype=dtype)

        input = self.align_with(input)

        EM.__init__(self, input=input, unit=unit, output=output, identify=identify)

        self._args = (input, iza, vza, raa, iaa, vaa, normalize, nbar,
                      angle_unit, align, dtype, unit, output, identify, name)

        self.name = name
        self.input_unit = unit
        self.output = output


