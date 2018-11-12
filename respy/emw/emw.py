from __future__ import division

import warnings

import numpy as np

from respy.emw.auxiliary import check_unit_frequency, check_unit_wavelength, BANDS, CONVERT_FREQ, CONVERT_WAVE
from respy.auxiliary import align_all

REGION = {"VIS": "OPTIC",
          "NIR": "OPTIC",
          "SWIR": "OPTIC",
          "MWIR": "THERMAL",
          "LWIR": "THERMAL",
          "L": "MICROWAVE",
          "S": "MICROWAVE",
          "C": "MICROWAVE",
          "X": "MICROWAVE",
          "Ku": "MICROWAVE",
          "K": "MICROWAVE",
          "Ka": "MICROWAVE",
          "V": "MICROWAVE",
          "W": "MICROWAVE",
          "D": "MICROWAVE"}

C = 299792458
PI = 3.14159265359


class EMW(object):
    def __init__(self, input, unit='GHz', output='cm'):
        """
        A class to describe electromagnetic waves.

        Parameters
        ----------
        input : int, float or array_like
            Frequency or wavelength
        unit : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'} or {'dm', 'nm', 'cm', 'mm', 'm', 'km', 'um'}
            Unit of input. Default is 'GHz'.
        output : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'} or {'dm', 'nm', 'cm', 'mm', 'm', 'km', 'um'}
            Unit of output. Default is 'cm'.

        Attributes
        ----------
        band : str
            Shows the band that the input belongs to.
        region : str
            Shows the region that the input belongs to.
        frequency : array_like
            Frequency.
        frequency_unit : str
            Unit of frequency.
        wavelength : array_like
            Wavelength.
        wavelength_unit : str
            Unit of wavelength.

        Note
        ----
        Frequency, wavelength, frequency_unit and wavelength_unit can be changed.
        
        """

        # Prepare Input Data and set values ----------------------------------------------------------------------------
        self.__unit = unit
        self.__output = output

        if unit in CONVERT_FREQ.keys() and output in CONVERT_WAVE.keys():
            self.__frequency_unit = unit
            self.__wavelength_unit = output

            if isinstance(input, str):
                self.__frequency = select_region(region=input, output=unit)
            else:
                self.__frequency = input

            self.__wavelength = self.__compute_wavelength()

        elif unit in CONVERT_WAVE.keys() and output in CONVERT_FREQ.keys():
            self.__frequency_unit = output
            self.__wavelength_unit = unit

            if isinstance(input, str):
                self.__wavelength = select_region(region=input, output=unit)
            else:
                self.__wavelength = input

            self.__frequency = self.__compute_frequency()

        else:
            raise ValueError("Input must be a frequency or a wavelength. "
                             "If input is a frequency, unit must be equal to {0}. "
                             "When entering a wavelength, unit must be equal to {1}.".format(str(CONVERT_FREQ.keys()),
                                                                                             str(CONVERT_WAVE.keys())))

        # Additional Calculation ---------------------------------------------------------------------------------------
        self.k0 = self.__compute_wavenumver()
        self.__region = which_region(self.__frequency, self.__frequency_unit)
        self.__band = which_band(self.__frequency, self.__frequency_unit)
        self.__array = np.asarray([self.__frequency, self.__wavelength, self.k0])
        self.array = self.__array

    # ------------------------------------------------------------------------------------------------------------------
    # Magic Methods
    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        vals = dict()
        vals['frequency'], vals['frequency_unit'] = self.iza.mean(), self.izaDeg.mean()
        vals['wavelength'], vals['wavelength_unit'] = self.vza.mean(), self.vzaDeg.mean()
        vals['wavenumber']  = self.raa.mean()
        vals['region'], vals['band'] = self.iaa.mean(), self.iaaDeg.mean()

        info = 'Class               : EMW\n' \
               'Mean frequency      : {frequency} {frequency_unit}\n' \
               'Mean wavelength     : {wavelength} {wavelength_unit}\n' \
               'Mean wavenumber     : {wavenumber} \n' \
               'Frequency is in {region} region at band {band}'.format(**vals)

        return info

    def __len__(self):
        return len(self.__frequency)

    # ------------------------------------------------------------------------------------------------------------------
    # Property Access
    # ------------------------------------------------------------------------------------------------------------------
    # Access to Array Specific Attributes ------------------------------------------------------------------------------
    @property
    def len(self):
        """
        Length of array

        Returns
        -------
        len : int
        """
        return len(self.__frequency)

    @property
    def shape(self):
        """
        Shape of array

        Returns
        -------
        shape : tuple
        """
        return self.__frequency.shape

    # ------------------------------------------------------------------------------------------------------------------
    # Property with Setter
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def band(self):
        return self.__band

    @property
    def region(self):
        return self.__region

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value
        self.__wavelength = self.__compute_wavelength()
        self.__k0 = self.__compute_wavenumver()
        self.__region = which_region(self.__frequency, self.__frequency_unit)
        self.__band = which_band(self.__frequency, self.__frequency_unit)

    @property
    def wavelength(self):
        return self.__wavelength

    @wavelength.setter
    def wavelength(self, value):
        self.__wavelength = value
        self.__frequency = self.__compute_frequency()
        self.__k0 = self.__compute_wavenumver()
        self.__region = which_region(self.__frequency, self.__frequency_unit)
        self.__band = which_band(self.__frequency, self.__frequency_unit)

    @property
    def frequency_unit(self):
        return self.__frequency_unit

    @frequency_unit.setter
    def frequency_unit(self, value):
        if value in CONVERT_FREQ.keys():
            self.__frequency = self.__convert_frequency(value)
            self.__frequency_unit = value
        else:
            raise ValueError("If input is a frequency, unit must be equal to {0}. ".format(str(CONVERT_FREQ.keys())))

    @property
    def wavelength_unit(self):
        return self.__wavelength_unit

    @wavelength_unit.setter
    def wavelength_unit(self, value):
        if value in CONVERT_WAVE.keys():
            self.__wavelength = self.__convert_wavelength(value)
            self.__wavelength_unit = value

        else:
            raise ValueError("When entering a wavelength, unit must be equal to {0}.".format(str(CONVERT_WAVE.keys())))

    # ------------------------------------------------------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------------------------------------------------------
    def align_with(self, value):
        """
        Align all angles with another array.

        Parameters
        ----------
        value : array_like

        Returns
        -------
        value : array_like
            Align value.

        Note
        ----
        If len(value) > EMW.shape[1] then the angles inside Angles class will be aligned and it has no effect on
        value. If len(value) < EMW.shape[1] the output of value will be have the same len as Angles and it has no
        effect on the angles within the Angles class.
        """
        # RAD Angles
        data = [item for item in self.__array]

        if isinstance(value, tuple) or isinstance(value, list):
            data = tuple(value) +  tuple(data, )
        else:
            data = (value,) + tuple(data, )

        data = align_all(data)

        self.__frequency, self.__wavelength, self.k0 = np.asarray(data[-3:])

        return data[0:-3]

    # ------------------------------------------------------------------------------------------------------------------
    # Private Methods
    # ------------------------------------------------------------------------------------------------------------------
    def __convert_frequency(self, value):
        return convert_frequency(frequency=self.__frequency, unit=self.__frequency_unit, output=value)

    def __convert_wavelength(self, value):
        return convert_wavelength(wavelength=self.__wavelength, unit=self.__wavelength_unit, output=value)

    def __update_variables(self):
        self.__frequency = self.__compute_frequency()
        self.__wavelength = self.__compute_wavelength()
        self.__k0 = self.__compute_wavenumver()

    def __compute_wavelength(self):
        return compute_wavelength(frequency=self.__frequency, unit=self.__frequency_unit, output=self.__wavelength_unit)

    def __compute_frequency(self):
        return compute_frequency(wavelength=self.__wavelength, unit=self.__wavelength_unit,
                                 output=self.__frequency_unit)

    def __compute_wavenumver(self):
        return compute_wavenumber(frequency=self.__frequency, unit=self.__frequency_unit, output=self.__wavelength_unit)


def compute_wavelength(frequency, unit='GHz', output="cm"):
    """
    Convert frequencies in wavelength.

    Parameters
    ----------
    frequency : int, float or array_like
        Frequency.
    unit : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'}
        Unit of entered frequency.
    output : {'dm', 'nm', 'cm', 'mm', 'm', 'km', 'um'}
        Unit of the wavelength.

    Returns
    -------
    Wavelength: float or array_like
    """
    check_unit_frequency(unit)
    check_unit_wavelength(output)

    if isinstance(frequency, np.ndarray):
        frequency = frequency.astype(float) * CONVERT_FREQ[unit]
    elif isinstance(frequency, float) or isinstance(frequency, int):
        frequency = float(frequency) * CONVERT_FREQ[unit]

    w = C / frequency

    return w * CONVERT_WAVE[output]


def compute_frequency(wavelength, unit='cm', output="GHz"):
    """
    Convert wavelengths in frequencies.

    Parameters
    ----------
    wavelength : int, float or array_like
        Wavelength.
    unit : {'dm', 'nm', 'cm', 'mm', 'm', 'km', 'um'}
        Unit of entered wavelength.
    output : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'}
        Unit of the frequency.

    Returns
    -------
    frequency: float or array_like
    """
    check_unit_frequency(output)
    check_unit_wavelength(unit)

    if isinstance(wavelength, np.ndarray):
        wavelength = wavelength.astype(float) / CONVERT_WAVE[unit]
    elif isinstance(wavelength, float) or isinstance(wavelength, int):
        wavelength = float(wavelength) / CONVERT_WAVE[unit]

    f = C / wavelength

    return f / CONVERT_FREQ[output]


def compute_wavenumber(frequency, unit='GHz', output='cm'):
    """
    Convert frequencies in free space wavenumbers.

    Parameters
    ----------
    frequency : int, float or array_like
        Frequency.
    unit : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'}
        Unit of entered frequency.
    output : {'dm', 'nm', 'cm', 'mm', 'm', 'km', 'um'}
        Unit of the wavelength.

    Returns
    -------
    wavenumber: float or array_like
    """
    return 2 * PI / compute_wavelength(frequency, unit=unit, output=output)


def convert_frequency(frequency, unit="GHz", output="Hz"):
    """
    Convert frequencies in other units.

    Parameters
    ----------
    frequency : int, float or array_like
        Frequency.
    unit : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'}
        Unit of entered frequency.
    output : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'}
        Unit of desired frequency.

    Returns
    -------
    frequency: float or array_like
    """
    check_unit_frequency(unit)
    check_unit_frequency(output)

    if isinstance(frequency, np.ndarray):
        frequency = frequency.astype(float) * CONVERT_FREQ[unit]
    elif isinstance(frequency, float) or isinstance(frequency, int):
        frequency = float(frequency) * CONVERT_FREQ[unit]

    return frequency / CONVERT_FREQ[output]


def convert_wavelength(wavelength, unit="cm", output="m"):
    """
    Convert wavelngth in other units.

    Parameters
    ----------
    wavelength : int, float or array_like
        wavelength.
    unit : {'dm', 'nm', 'cm', 'mm', 'm', 'km', 'um'}
        Unit of entered frequency.
    output : {'dm', 'nm', 'cm', 'mm', 'm', 'km', 'um'}
        Unit of desired frequency.

    Returns
    -------
    wavelength: float or array_like
    """
    check_unit_wavelength(unit)
    check_unit_wavelength(output)

    if isinstance(wavelength, np.ndarray):
        wavelength = wavelength.astype(float) * CONVERT_WAVE[output]
    elif isinstance(wavelength, float) or isinstance(wavelength, int):
        wavelength = float(wavelength) * CONVERT_WAVE[output]

    return wavelength / CONVERT_WAVE[unit]


def select_band(band="L", output="GHz"):
    """
    Select a band from the EM spectrum.

    Parameters
    ----------
    band : {"VIS", "NIR", "SWIR", "MWIR", "LWIR", "L", "S", "C", "X", "Ku", "K", "Ka", "V", "W", "D"}
        Region of the EM spectrum.
    output : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'}
        Output unit.

    Returns
    -------
    region : array_like

    Note
    ----
    This is only a auxiliary function. Thus the output is only as frequency. The function 'select_region'
    is more convenient to use which allows a output in wavelength.

    See Also
    --------
    respy.emw.select_region

    """
    # ---- Optical Region ----
    if band is "VIS":
        VIS = np.arange(400., 751., 1)
        return compute_frequency(VIS[np.argsort(-VIS)], 'nm', output)
    elif band is "NIR":
        NIR = np.arange(751., 1001., 1)
        return compute_frequency(NIR[np.argsort(-NIR)], 'nm', output)
    elif band is "SWIR":
        SWIR = np.arange(1001., 2501., 1)
        return compute_frequency(SWIR[np.argsort(-SWIR)], 'nm', output)
    elif band is "MWIR":
        MWIR = np.arange(3000., 5001., 1)
        return compute_frequency(MWIR[np.argsort(-MWIR)], 'nm', output)
    elif band is "LWIR":
        LWIR = np.arange(8000., 12001., 1)
        return compute_frequency(LWIR[np.argsort(-LWIR)], 'nm', output)

    # ---- Microwave Region ----
    elif band is "L":
        return (np.arange(1, 2.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif band is "S":
        return (np.arange(2.1, 4.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif band is "C":
        return (np.arange(4.1, 8.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif band is "X":
        return (np.arange(8.1, 12.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif band is "Ku":
        return (np.arange(12.1, 18.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif band is "K":
        return (np.arange(18.1, 26.6, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif band is "Ka":
        return (np.arange(26.6, 40.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif band is "V":
        return (np.arange(50.1, 75.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif band is "W":
        return (np.arange(75.1, 110.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]
    elif band is "D":
        return (np.arange(110.1, 170.1, 0.1) * CONVERT_FREQ['GHz']) / CONVERT_FREQ[output]

    else:
        raise ValueError("Supported regions are  {0}.".format(str(BANDS)))


EMS = {"VIS": select_band("VIS"),
       "NIR": select_band("NIR"),
       "SWIR": select_band("SWIR"),
       "MWIR": select_band("MWIR"),
       "LWIR": select_band("LWIR"),
       "L": select_band("L"),
       "S": select_band("S"),
       "C": select_band("C"),
       "X": select_band("X"),
       "Ku": select_band("Ku"),
       "K": select_band("K"),
       "Ka": select_band("Ka"),
       "V": select_band("V"),
       "W": select_band("W"),
       "D": select_band("D")}


def select_region(region, output="GHz"):
    """
    Select a region from the electromagnetic field.

    Parameters
    ----------
    region : str
        Region of the EM field. Possible combinations:
            * 'RADAR' : Output from L - X band.
            * 'OPTIC' : Output from VIS, NIR and SWIR band.
            * 'THERMAL' : Output from MWIR - LWIR.
            * 'L'-'D' : RADAR regions like "L", "S", "C", "X", "Ku", "K", "Ka", "V", "W", "D".
            * 'VIS' - 'LWIR' : Optical and thermal regions like "VIS", "NIR", "SWIR", "MWIR", "LWIR".
    output : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'} or {'dm', 'nm', 'cm', 'mm', 'm', 'km', 'um'}
        Output unit.

    Returns
    -------
    Range : array_like
    """
    if region is "RADAR":
        Lb = EMS["L"]
        Sb = EMS["S"]
        Cb = EMS["C"]
        Xb = EMS["X"]

        output_region = np.concatenate((Lb, Sb, Cb, Xb))

    elif region is "OPTIC":
        VIS = EMS["VIS"]
        NIR = EMS["NIR"]
        SWIR = EMS["SWIR"]
        output_region = np.concatenate((SWIR, NIR, VIS))

    elif region is "THERMAL":
        MWIR = EMS["MWIR"]
        LWIR = EMS["LWIR"]
        output_region = np.concatenate((LWIR, MWIR))

    elif isinstance(region, list):
        output_list = list()

        for item in region:
            try:
                output_list.append(select_band(band=item, output='GHz'))

            except ValueError:
                raise ValueError("The input region is not valid. It must be 'RADAR', 'OPTIC', 'THERMAL', the RADAR "
                                 "bans ('L' - 'D'), 'VIS', 'NIR', 'SWIR', 'MWIR', 'LWIR' or a list with regions."
                                 "The actual region is {0}".format(str(region)))

        output_list = tuple(output_list)
        output_region = np.concatenate(output_list)

    else:
        try:
            output_region = EMS[region]
        except KeyError:
            raise ValueError("The input region is not valid. It must be 'RADAR', 'OPTIC', 'THERMAL', the RADAR "
                             "bans ('L' - 'D') or 'VIS', 'NIR', 'SWIR', 'MWIR' and 'LWIR'."
                             "The actual region is {0}".format(str(region)))

    if output in CONVERT_WAVE.keys():
        output_region = compute_wavelength(output_region, unit="GHz", output=output)
        output_region = output_region[np.argsort(output_region)]

    elif output in CONVERT_FREQ.keys():
        output_region = convert_frequency(output_region, 'GHz', output=output)

    else:
        raise ValueError(
            "The parameter output must be {0} or {1}. The actual output is {2}".format(str(CONVERT_FREQ.keys()),
                                                                                       str(CONVERT_WAVE.keys()),
                                                                                       str(output)))

    return output_region


def which_band(input, unit='GHz'):
    """
    A function to find out which band a frequency or wavelength belongs to.

    Parameters
    ----------
    input : int, float or array_like
        Frequency or wavelength.
    unit : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'} or {'dm', 'nm', 'cm', 'mm', 'm', 'km', 'um'}
        Output unit.

    Returns
    -------
    band : str
        Output contains "VIS", "NIR", "SWIR", "MWIR", "LWIR", "L", "S", "C", "X", "Ku", "K", "Ka", "V", "W", "D".
    """
    if unit in CONVERT_FREQ.keys():
        frequence = convert_frequency(input, unit=unit, output='GHz')

    elif unit in CONVERT_WAVE.keys():
        frequence = compute_frequency(input, unit, 'GHz')
    else:
        raise ValueError("Input must be a frequency or a wavelength. "
                         "If input is a frequency, unit must be equal to {0}. "
                         "When entering a wavelength, unit must be equal to {1}.".format(str(CONVERT_FREQ.keys()),
                                                                                         str(CONVERT_WAVE.keys())))

    if isinstance(frequence, np.ndarray) and len(frequence) > 1:
        item_list = list()
        for i in range(frequence.shape[0]):
            for item in BANDS:
                if EMS[item][0] <= frequence[i] <= EMS[item][-1]:
                    item_list.append(item)
                else:
                    pass

        item_list = list(set(item_list))

    else:
        item_list = list()
        for item in BANDS:
            if EMS[item][0] <= frequence <= EMS[item][-1]:
                item_list.append(item)
            else:
                pass

        item_list = list(set(item_list))

    if len(item_list) == 0:
        warnings.warn("Input region not supported. Returning None.")
        return None

    elif len(item_list) == 1:
        return item_list[0]

    else:
        return item_list


def which_region(input, unit='GHz'):
    """
    A function to find out which region a frequency or wavelength belongs to.

    Parameters
    ----------
    input : int, float or array_like
        Frequency or wavelength.
    unit : {'Hz', 'PHz', 'kHz', 'daHz', 'MHz', 'THz', 'hHz', 'GHz'} or {'dm', 'nm', 'cm', 'mm', 'm', 'km', 'um'}
        Output unit.

    Returns
    -------
    region : str
        Output contains 'OPTIC', 'MICROWAVE'.
    """
    if isinstance(input, np.ndarray) and len(input) > 1:
        band_list = list()

        for i in range(input.shape[0]):
            band_list.append(which_band(input[i], unit))

        region_list = list()
        for item in band_list:
            if item is not None:
                region_list.append(REGION[item])
            else:
                region_list.append(None)

            region_list = list(set(region_list))

        if len(region_list) == 1:
            region_list = region_list[0]
        else:
            pass

    else:
        band = which_band(input, unit)
        if band is not None:
            region_list = REGION[band]
        else:
            region_list = None

    return region_list
