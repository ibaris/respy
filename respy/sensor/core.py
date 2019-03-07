# -*- coding: utf-8 -*-
"""
Created on 26.02.2019 by Ismail Baris
"""
from __future__ import division
from respy import Angles, EM
import numpy as np
from respy.units import Units


class Sensor(Angles, EM):
    def __init__(self, input, iza, vza, raa=None, iaa=None, vaa=None, normalize=False, nbar=0.0,
                 angle_unit='DEG', align=True, dtype=np.double, unit='GHz', output='cm', identify=False, name=None):

        Angles.__init__(self, iza=iza, vza=vza, raa=raa, iaa=iaa, vaa=vaa, normalize=normalize, nbar=nbar,
                        angle_unit=angle_unit, align=align, dtype=dtype)

        EM.__init__(self, input=input, unit=unit, output=output, identify=identify)
        self.name = name
        self.input_unit = unit
        self.output = output

    def __repr__(self):
        prefix = '<{0} '.format(self.__class__.__name__)
        sep = ', '
        if self.input_unit in Units.frequency.keys():
            arrstr = np.array2string(self.frequency.value,
                                     separator=sep,
                                     prefix=prefix)

            unit = self.frequency.unitstr

        else:
            arrstr = np.array2string(self.wavelength.value,
                                     separator=sep,
                                     prefix=prefix)

            unit = self.wavelength.unitstr

        if self.name is None or self.name is b'':
            return '{0}{1} [{2}]>'.format(prefix, arrstr, unit)
        else:
            return '{0}{1} {2} in [{3}]>'.format(prefix, arrstr, self.name, unit)
