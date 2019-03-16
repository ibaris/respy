from __future__ import division

from numpy import cos, log10, errstate, nan_to_num
import numpy as np
import respy.constants as const
from respy.util import rad, __ANGLE_UNIT_DEG__, __ANGLE_UNIT_RAD__
from respy.units import Quantity


class Conversion(object):
    def __init__(self, value, vza=None, value_unit="BRDF", angle_unit='RAD', quantity=False):
        """
        Conversion of BRDF, BRF, BSC and BSC in dB.

        Parameters
        ----------
        value : float, array_like
            Input value in BRDF, BRF, BSC or BSCdB. See parameter value_unit.
        vza : int, float, array_like
            Viewing zenith angle in DEG or RAD. See parameter angle_unit.
        value_unit : {'I', 'BRDF', 'BRF', 'BSC', 'BSCdB', 'BSCdb', 'brdf', 'brf', 'bsc', 'bscdb'}
            The unit of input value:
            * I or BRDF : Bidirectional Reflectance Distribution Function (Intensity) (default).
            * BRF : Bidirectional Reflectance Factor.
            * BSC : Back Scattering Coefficient (no unit).
            * BSCdB : Back Scattering Coefficient in dB.
        angle_unit : {'DEG', 'RAD', 'deg', 'rad'}, optional
            * 'DEG': Input angle in [DEG].
            * 'RAD': Input angle  in [RAD] (default).

        Attributes
        ----------
        I : array_like or respy.unit.quantity.Quantity
            Intensity (BRDF) value.
        BRF : array_like or respy.unit.quantity.Quantity
            BRF value.
        BSC : array_like or respy.unit.quantity.Quantity
            BSC value.
        BSCdB : array_like or respy.unit.quantity.Quantity
            BSC value in dB.
        value : array_like
            All values in an array of type np.array([I, BRF, BSC, BSCdB])

        Methods
        -------
        Conversion.dB : Convert linear to dB
        Conversion.linear : Convert dB to linear.

        See Also
        --------
        respy.dB
        respy.linear
        respy.BRDF
        respy.BRF
        respy.BSC
        """
        self.value_unit = value_unit
        self.quantity = quantity
        self.angle_unit = angle_unit


        if self.value_unit is "BRDF":
            self.I = value
            self.BRF = Conversion.BRDF_to_BRF(value)

            if vza is not None:
                self.BSC = Conversion.BRDF_to_BSC(value, vza, self.angle_unit)
                self.BSCdB = Conversion.dB(Conversion.BRDF_to_BSC(value, vza, self.angle_unit))

            else:
                self.BSC = np.zeros_like(value)
                self.BSCdB = np.zeros_like(value)

        elif self.value_unit is "BSC":
            self.BSC = value
            self.BSCdB = Conversion.dB(value)

            if vza is not None:
                self.I = Conversion.BSC_to_BRDF(value, vza, self.angle_unit)
                self.BRF = Conversion.BRDF_to_BRF(self.I)
            else:
                self.I = np.zeros_like(value)
                self.BRF = np.zeros_like(value)

        elif self.value_unit is "BSCdB":
            self.BSCdB = value
            self.BSC = Conversion.linear(value)

            if vza is not None:
                self.I = Conversion.BSC_to_BRDF(value, vza, self.angle_unit)
                self.BRF = Conversion.BRDF_to_BRF(self.I)
            else:
                self.I = np.zeros_like(value)
                self.BRF = np.zeros_like(value)

        elif self.value_unit is "BRF":
            self.BRF = value
            self.I = value / const.pi

            if vza is not None:
                self.BSC = Conversion.BRDF_to_BSC(value, vza, self.angle_unit)
                self.BSCdB = Conversion.dB(Conversion.BRDF_to_BSC(value, vza, self.angle_unit))

            else:
                self.BSC = np.zeros_like(value)
                self.BSCdB = np.zeros_like(value)

        else:
            raise ValueError("the unit of value must be 'BRDF', 'BRF', 'BSC' or 'BSCdB'")

        if quantity:
            self.BSC = Quantity(self.BSC, name='Backscattering Coefficient', constant=True)
            self.BSCdB = Quantity(self.BSCdB, unit='dB', name='Backscattering Coefficient', constant=True)
            self.I = Quantity(self.I, name='Intensity', constant=True)
            self.BRF = Quantity(self.BRF, name='Bidirectional Reflectance Factor', constant=True)
        else:
            pass

        self.value = np.array([self.I, self.BRF, self.BSC, self.BSCdB])

    # --------------------------------------------------------------------------------------------------------
    # Magic Methods
    # --------------------------------------------------------------------------------------------------------
    def __repr__(self):
        prefix = '<{0} '.format(self.__class__.__name__)
        sep = ','

        if self.quantity:
            arrstr_bsc = np.array2string(self.BSC.value,
                                         separator=sep,
                                         prefix=prefix)

            arrstr_dB = np.array2string(self.BSCdB.value,
                                        separator=sep,
                                        prefix=prefix)

            arrstr_I = np.array2string(self.I.value,
                                       separator=sep,
                                       prefix=prefix)

            arrstr_BRF = np.array2string(self.BRF.value,
                                         separator=sep,
                                         prefix=prefix)

            bsc = '{0}{1} Backscattering Coefficient in [{2}]>'.format(prefix, arrstr_bsc, self.BSC.unitstr)
            bscdb = '{0}{1} Backscattering Coefficient in [{2}]>'.format(prefix, arrstr_dB, self.BSCdB.unitstr)
            I = '{0}{1} Intensity in [{2}]>'.format(prefix, arrstr_I, self.I.unitstr)
            BRF = '{0}{1} Bidirectional Reflectance Factor in [{2}]>'.format(prefix, arrstr_BRF, self.BRF.unitstr)


        else:
            arrstr_bsc = np.array2string(self.BSC,
                                         separator=sep,
                                         prefix=prefix)

            arrstr_dB = np.array2string(self.BSCdB,
                                        separator=sep,
                                        prefix=prefix)

            arrstr_I = np.array2string(self.I,
                                       separator=sep,
                                       prefix=prefix)

            arrstr_BRF = np.array2string(self.BRF,
                                         separator=sep,
                                         prefix=prefix)

            bsc = '{0}{1} Backscattering Coefficient in [{2}]>'.format(prefix, arrstr_bsc, '[-]')
            bscdb = '{0}{1} Backscattering Coefficient in [{2}]>'.format(prefix, arrstr_dB, '[dB]')
            I = '{0}{1} Intensity in [{2}]>'.format(prefix, arrstr_I, '[-]')
            BRF = '{0}{1} Bidirectional Reflectance Factor in [{2}]>'.format(prefix, arrstr_BRF, '[-]')

        return I + '\n' + BRF + '\n' + bsc + '\n' + bscdb

    def __getitem__(self, item):
        return self.value[item]

    @staticmethod
    def dB(x):
        """
        Convert a linear value to dB.
        """
        with errstate(invalid='ignore'):
            return nan_to_num(10 * log10(x))

    @staticmethod
    def linear(x):
        """
        Convert a dB value in linear.
        """
        return 10 ** (x / 10)

    @staticmethod
    def BSC_to_BRDF(BSC, vza, angle_unit='RAD'):
        """
        Convert a Radar Backscatter Coefficient (BSC) into a BRDF.

        Note
        -----
        Hot spot direction is vza == iza and raa = 0.0

        Parameters
        ----------
        BSC : int, float or array_like
            Radar Backscatter Coefficient (sigma 0).
        vza : int, float or array_like
            View or scattering zenith angle.
        angle_unit : {'DEG', 'RAD'} (default = 'RAD'), optional
            * 'DEG': All input angles (iza, vza, raa) are in [DEG].
            * 'RAD': All input angles (iza, vza, raa) are in [RAD].

        Returns
        -------
        BRDF value : int, float or array_like

        """
        if angle_unit in __ANGLE_UNIT_RAD__:
            return BSC / (cos(vza) * (4 * const.pi))

        elif angle_unit in __ANGLE_UNIT_DEG__:
            return BSC / (cos(rad(vza)) * (4 * const.pi))
        else:
            raise ValueError("angle_unit must be 'RAD' or 'DEG'")

    @staticmethod
    def BRDF_to_BRF(BRDF):
        """
        Convert a BRDF into a BRF.

        Note
        -----
        Hot spot direction is vza == iza and raa = 0.0

        Parameters
        ----------
        BRDF : int, float or array_like
            BRDF value.

        Returns
        -------
        BRF value : int, float or array_like

        """
        return const.pi * BRDF

    @staticmethod
    def BRDF_to_BSC(BRDF, vza, angle_unit='RAD'):
        """
        Convert a BRDF in to a Radar Backscatter Coefficient (BSC).

        Note
        -----
        Hot spot direction is vza == iza and raa = 0.0

        Parameters
        ----------
        BRDF : int, float or array_like
            Intensity as a BRDF.
        vza : int, float or array_like
            View or scattering zenith angle.
        angle_unit : {'DEG', 'RAD'} (default = 'RAD'), optional
            * 'DEG': All input angles (iza, vza, raa) are in [DEG].
            * 'RAD': All input angles (iza, vza, raa) are in [RAD].

        Returns
        -------
        BRDF value : int, float or array_like

        """
        if angle_unit in __ANGLE_UNIT_RAD__:
            return BRDF * cos(vza) * 4 * const.pi

        elif angle_unit in __ANGLE_UNIT_DEG__:
            return BRDF * cos(rad(vza)) * (4 * const.pi)
        else:
            raise ValueError("angle_unit must be 'RAD' or 'DEG'")
