from __future__ import division
import warnings

from numpy import cos, pi, log10, errstate, nan_to_num, arange, concatenate, argsort, ndarray

from radarpy.auxiliary import rad, check_unit_frequency, check_unit_wavelength, CONVERT_FREQ, CONVERT_WAVE

C = 299792458
PI = 3.14159265359


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
        return BSC / (cos(vza) * (4 * pi))

    elif angle_unit == 'DEG':
        return BSC / (cos(rad(vza)) * (4 * pi))
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
    return pi * BRDF


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
        return BRDF * cos(vza) * 4 * pi

    elif angle_unit == 'DEG':
        return BRDF * cos(rad(vza)) * (4 * pi)
    else:
        raise ValueError("angle_unit must be 'RAD' or 'DEG'")