from numpy import cos, pi, log10, errstate, nan_to_num

from .auxiliary import rad

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


def wavelength(frequency, unit='GHz', output="cm"):
    """
    Convert frequencies in wavelength.

    Parameters
    ----------
    frequency : int, float or array_like
        Frequency.
    unit : {'Hz', 'MHz', 'GHz', 'THz'}
        Unit of entered frequency.
    output : {'m', 'cm', 'nm'}
        Unit of the wavelength.

    Returns
    -------
    Wavelength: float or array_like
    """

    if unit is "Hz":
        pass
    elif unit is "MHz":
        frequency *= 1e6
    elif unit is "GHz":
        frequency *= 1e9
    elif unit is "THz":
        frequency *= 1e12
    else:
        raise ValueError("unit must be MHz, GHz or THz.")

    w = C / frequency

    if output is "m":
        pass
    elif output is "cm":
        w *= 100
    elif output is "nm":
        w *= 1e+9
    else:
        raise ValueError("output must be m, cm or nm.")

    return w


def frequency(wavelength, unit='cm', output="GHz"):
    """
    Convert wavelengths in frequencies.

    Parameters
    ----------
    wavelength : int, float or array_like
        Wavelength.
    unit : {'m', 'cm', 'nm'}
        Unit of entered wavelength.
    output : {'Hz', 'MHz', 'GHz', 'THz'}
        Unit of the frequency.

    Returns
    -------
    frequency: float or array_like
    """

    if unit is "m":
        pass
    elif unit is "cm":
        wavelength /= 100
    elif unit is "nm":
        wavelength /= 1e+9
    else:
        raise ValueError("output must be m, cm or nm.")

    f = C / wavelength

    if output is "Hz":
        pass
    elif output is "MHz":
        f /= 1e6
    elif output is "GHz":
        f /= 1e9
    elif output is "THz":
        f /= 1e12
    else:
        raise ValueError("unit must be MHz, GHz or THz.")

    return f


def wavenumber(frequency, unit='GHz', output='cm'):
    """
    Convert frequencies in free space wavenumbers.

    Parameters
    ----------
    frequency : int, float or array_like
        Frequency.
    unit : {'Hz', 'MHz', 'GHz', 'THz'}
        Unit of entered frequency.
    output : {'m', 'cm', 'nm'}
        Unit of the wavelength.

    Returns
    -------
    wavenumber: float or array_like
    """
    return 2 * PI / wavelength(frequency, unit=unit, output=output)
