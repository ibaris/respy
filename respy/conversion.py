from __future__ import division

from numpy import cos, log10, errstate, nan_to_num

from respy.auxiliary import rad, PI


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
            self.BSC = BSC(value, vza, self.angle_unit)
            self.BSCdB = dB(BSC(value, vza, self.angle_unit))
            self.BRF = BRF(value)

        elif self.value_unit is "BSC":
            self.BSC = value
            self.BRDF = BRDF(value, vza, self.angle_unit)
            self.BRF = BRF(self.BRDF)
            self.BSCdB = dB(value)

        elif self.value_unit is "BSCdB":
            self.BSCdB = value
            self.BSC = linear(value)
            self.BRDF = BRDF(self.BSC, vza, self.angle_unit)
            self.BRF = BRF(self.BRDF)

        elif self.value_unit is "BRF":
            self.BRF = value
            self.BRDF = value / PI
            self.BSC = BSC(self.BRDF, vza, self.angle_unit)
            self.BSCdB = dB(BSC(self.BRDF, vza, self.angle_unit))

        else:
            raise ValueError("the unit of value must be 'BRDF', 'BRF', 'BSC' or 'BSCdB'")


    @staticmethod
    def dB(x):
        return dB(x)

    @staticmethod
    def linear(x):
        return linear(x)


def dB(x):
    """
    Convert a linear value to dB.
    """
    with errstate(invalid='ignore'):
        return nan_to_num(10 * log10(x))


def linear(x):
    """
    Convert a dB value in linear.
    """
    return 10 ** (x / 10)


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
    if angle_unit == 'RAD':
        return BSC / (cos(vza) * (4 * PI))

    elif angle_unit == 'DEG':
        return BSC / (cos(rad(vza)) * (4 * PI))
    else:
        raise ValueError("angle_unit must be 'RAD' or 'DEG'")


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
    return PI * BRDF


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
    if angle_unit == 'RAD':
        return BRDF * cos(vza) * 4 * PI

    elif angle_unit == 'DEG':
        return BRDF * cos(rad(vza)) * (4 * PI)
    else:
        raise ValueError("angle_unit must be 'RAD' or 'DEG'")
