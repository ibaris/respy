from __future__ import division

from numpy import cos, log10, errstate, nan_to_num

import respy.constants as const
from respy.util import rad, __ANGLE_UNIT_DEG__, __ANGLE_UNIT_RAD__


class Conversion(object):
    def __init__(self, value, vza, value_unit="BRDF", angle_unit='RAD'):
        """
        Conversion of BRDF, BRF, BSC and BSC in dB.

        Parameters
        ----------
        value : float, array_like
            Input value in BRDF, BRF, BSC or BSCdB. See parameter value_unit.
        vza : int, float, array_like
            Viewing zenith angle in DEG or RAD. See parameter angle_unit.
        value_unit : {'BRDF', 'BRF', 'BSC', 'BSCdB'}
            The unit of input value:
            * BRDF : Bidirectional Reflectance Distribution Function (Intensity) (default).
            * BRF : Bidirectional Reflectance Factor.
            * BSC : Back Scattering Coefficient (no unit).
            *BSCdB : Back Scattering Coefficient in dB.
        angle_unit : {'DEG', 'RAD', 'deg', 'rad'}, optional
            * 'DEG': Input angle in [DEG].
            * 'RAD': Input angle  in [RAD] (default).

        Attributes
        ----------
        Conversion.BRDF : array_like
            BRDF value.
        Conversion.BRF : array_like
            BRF value.
        Conversion.BSC : array_like
            BSC value.
        Conversion.BSCdB : array_like
            BSC value in dB.

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

        if angle_unit is "rad":
            angle_unit = "RAD"
        elif angle_unit is "deg":
            angle_unit = "DEG"

        self.angle_unit = angle_unit

        if self.value_unit is "BRDF":
            self.BRDF = value
            self.BSC = Conversion.BSC(value, vza, self.angle_unit)
            self.BSCdB = Conversion.dB(Conversion.BSC(value, vza, self.angle_unit))
            self.BRF = Conversion.BRF(value)

        elif self.value_unit is "BSC":
            self.BSC = value
            self.BRDF = Conversion.BRDF(value, vza, self.angle_unit)
            self.BRF = Conversion.BRF(self.BRDF)
            self.BSCdB = Conversion.dB(value)

        elif self.value_unit is "BSCdB":
            self.BSCdB = value
            self.BSC = Conversion.linear(value)
            self.BRDF = Conversion.BRDF(self.BSC, vza, self.angle_unit)
            self.BRF = Conversion.BRF(self.BRDF)

        elif self.value_unit is "BRF":
            self.BRF = value
            self.BRDF = value / const.pi
            self.BSC = Conversion.BSC(self.BRDF, vza, self.angle_unit)
            self.BSCdB = Conversion.dB(Conversion.BSC(self.BRDF, vza, self.angle_unit))

        else:
            raise ValueError("the unit of value must be 'BRDF', 'BRF', 'BSC' or 'BSCdB'")

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
    def BRDF(BSC, vza, angle_unit='RAD'):
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
    def BRF(BRDF):
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
    def BSC(BRDF, vza, angle_unit='RAD'):
        """
        Convert a BRDF in to a Radar Backscatter Coefficient (BSC).

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
            return BRDF * cos(vza) * 4 * const.pi


        elif angle_unit in __ANGLE_UNIT_DEG__:
            return BRDF * cos(rad(vza)) * (4 * const.pi)
        else:
            raise ValueError("angle_unit must be 'RAD' or 'DEG'")
