from __future__ import division
import warnings

from numpy import cos, pi, log10, errstate, nan_to_num, arange, concatenate, argsort, ndarray

from .auxiliary import rad, check_unit_frequency, check_unit_wavelength, CONVERT_FREQ, CONVERT_WAVE

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
    check_unit_frequency(unit)
    check_unit_wavelength(output)

    if isinstance(frequency, ndarray):
        frequency = frequency.astype(float) * CONVERT_FREQ[unit]
    elif isinstance(frequency, float) or isinstance(frequency, int):
        frequency = float(frequency) * CONVERT_FREQ[unit]

    w = C / frequency

    return w * CONVERT_WAVE[output]


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
    check_unit_frequency(output)
    check_unit_wavelength(unit)

    if isinstance(wavelength, ndarray):
        wavelength = wavelength.astype(float) / CONVERT_WAVE[unit]
    elif isinstance(wavelength, float) or isinstance(wavelength, int):
        wavelength = float(wavelength) / CONVERT_WAVE[unit]

    f = C / wavelength

    return f / CONVERT_FREQ[output]


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


def convert_frequency(frequency, unit="GHz", output="Hz"):
    """
    Convert frequencies in other units.

    Parameters
    ----------
    frequency : int, float or array_like
        Frequency.
    unit : {'Hz', 'MHz', 'GHz', 'THz'}
        Unit of entered frequency.
    output : {'Hz', 'MHz', 'GHz', 'THz'}
        Unit of desired frequency.

    Returns
    -------
    frequency: float or array_like
    """
    check_unit_frequency(unit)
    check_unit_frequency(output)

    if isinstance(frequency, ndarray):
        frequency = frequency.astype(float) * CONVERT_FREQ[unit]
    elif isinstance(frequency, float) or isinstance(frequency, int):
        frequency = float(frequency) * CONVERT_FREQ[unit]

    return frequency / CONVERT_FREQ[output]


def select_region(region, output="GHz"):
    """
    Select a region from the electromagnetic field.

    Parameters
    ----------
    region : str
        Region of the EM field. Possible combinations:
            * 'RADAR' : Output from L - X band.
            * 'OPTIC' : Output from VIS - NIR.
            * 'xyz' : Output of x, y and z. Possible combinations are 'LSCX', which is the RADAR range, 'LS' for
                      L and S band, 'CX' for C and X band and so foth.
    output : {'Hz', 'MHz', 'GHz', 'THz', 'm', 'cm', 'nm'}
        Output unit.

    Returns
    -------
    Range : array_like

    """
    if region is "RADAR":
        Lb = band(region="L", output="GHz")
        Sb = band(region="S", output="GHz")
        Cb = band(region="C", output="GHz")
        Xb = band(region="X", output="GHz")

        output_region = concatenate((Lb, Sb, Cb, Xb))

    elif region is "OPTIC":
        VIS = band(region="VIS", output="GHz")
        NIR = band(region="NIR", output="GHz")

        output_region = concatenate((NIR, VIS))

    else:
        region = list(region)
        output_list = list()

        for item in region:
            try:
                output_list.append(band(region=item, output='GHz'))

            except ValueError:
                raise ValueError("The input region is not valid. It must be a combination of letters 'L', 'S', 'C' " +
                                 "'X' or the words 'RADAR' or 'OPTIC'. The actual region is {0}".format(str(region)))

        output_list = tuple(output_list)
        output_region = concatenate(output_list)

    if 'm' in output or 'cm' in output or 'nm' in output:
        output_region = wavelength(output_region, unit="GHz", output=output)
        output_region = output_region[argsort(output_region)]

    elif 'Hz' in output or 'MHz' in output or 'GHz' in output or 'THz' in output:
        output_region = convert_frequency(output_region, 'GHz', output=output)

    else:
        raise ValueError("The parameter output must be Hz, MHz, GHz, THz, nm, cm or m. The actual output is {0}",
                         format(str(output)))

    return output_region


def which_band(input, unit='GHz'):
    if 'Hz' in unit or 'MHz' in unit or 'GHz' in unit or 'THz' in unit:
        frequence = convert_frequency(input, unit=unit, output='GHz')

    elif 'm' in unit or 'cm' in unit or 'nm' in unit:
        frequence = frequency(input, unit, 'GHz')

    Lb = band(region="L", output="GHz")
    Sb = band(region="S", output="GHz")
    Cb = band(region="C", output="GHz")
    Xb = band(region="X", output="GHz")
    VIS = band(region="VIS", output="GHz")
    NIR = band(region="NIR", output="GHz")

    if Lb[0] <= frequence <= Lb[-1]:
        return "L"
    elif Sb[0] <= frequence <= Sb[-1]:
        return "S"
    elif Cb[0] <= frequence <= round(Cb[-1], 2):
        return "C"
    elif Xb[0] <= frequence <= round(Xb[-1], 2):
        return "X"
    elif VIS[0] <= frequence <= VIS[-1]:
        return "VIS"
    elif NIR[0] <= frequence <= NIR[-1]:
        return "NIR"
    else:
        warnings.warn("Frequency not in RADAR or OPTIC range. Returning None.")
        return None


def band(region="L", output="GHz"):
    """
    Select a band from the EM spectrum.

    Parameters
    ----------
    region : {'L', 'S', 'C', 'X', 'VIS', 'NIR'}
        Region of the EM spectrum.
    output : {'Hz', 'MHz', 'GHz', 'THz'}
    Output unit.

    Returns
    -------
    region : array_like

    """
    if region is "L":
        return (arange(1, 2.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif region is "S":
        return (arange(2.1, 4.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif region is "C":
        return (arange(4.1, 8.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif region is "X":
        return (arange(8.1, 12.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif region is "VIS":
        VIS = arange(400., 751., 1)
        return frequency(VIS[argsort(-VIS)], 'nm', output)
    elif region is "NIR":
        NIR = arange(751., 2501., 1)
        return frequency(NIR[argsort(-NIR)], 'nm', output)
    else:
        raise ValueError("The parameter region must be L, S, C, X, VIS or NIR")


def volume_eq_radius(h, d):
    n = 1 / 3
    ar = h / d  # axis ratio
    V = (4 / 3) * PI * h * d / 2  # volume of particle
    rv = ((6 / PI * V) ** n) / 2  # volume equivalent radius

    return ar, rv
