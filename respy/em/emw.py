from __future__ import division

import numpy as np

import respy.constants as const
from respy.util import align_all
from respy.units import Quantity
from respy.units import Units
from respy.units.util import def_unit, DimensionError
from respy.em.util import __REGION__, __BANDS__, __WHICH__BAND__, __WHICH__REGION__
from respy.units.util import DimensionError, UnitError


class EM(object):
    def __init__(self, input, unit='GHz', output='cm'):
        """
        A class to describe electromagnetic waves.

        Parameters
        ----------
        input : int, float, np.ndarray, respy.units.quantity.Quantity
            Frequency or wavelength.
        unit : str, respy.units.Units, sympy.physics.units.quantities.Quantity
            Unit of input. Default is 'GHz'.
        output : str, respy.units.Units, sympy.physics.units.quantities.Quantity
            Unit of output. Default is 'cm'.

        Attributes
        ----------
        band : str
            Shows the band that the input belongs to.
        region : str
            Shows the region that the input belongs to.
        frequency : respy.units.quantity.Quantity
            Frequency.
        wavelength : respy.units.quantity.Quantity
            Wavelength.
        len : int
            Length of array.
        shape : tuple
            Shape of array.

        Methods
        -------

        Note
        ----
        Frequency, wavelength, frequency_unit and wavelength_unit can be changed.
        
        """

        # Prepare Input Data and set values ----------------------------------------------------------------------------
        input = np.asarray(input).flatten()

        # Self Definitions ---------------------------------------------------------------------------------------------
        self.__unit = unit
        self.__output = output

        # Assign Input Parameter ---------------------------------------------------------------------------------------
        if input.__class__.__name__ is 'Quantity':
            if str(input.dimension) == 'frequency':
                self.__frequency_unit = input.unit

                if output in Units.length.keys():
                    self.__wavelength_unit = output
                else:
                    raise UnitError("Output unit {} is not a valid unit if input is a frequency.".format(str(output)))

                self.__frequency = input
                self.__wavelength = EM.compute_wavelength(self.__frequency, self.__frequency_unit,
                                                          output=self.__wavelength_unit)

        elif unit in Units.frequency.keys() and output in Units.length.keys():
            self.__frequency_unit = unit
            self.__wavelength_unit = output

            self.__frequency = Quantity(input, unit=self.__frequency_unit)
            self.__wavelength = EM.compute_wavelength(self.__frequency, self.__frequency_unit, output=self.__wavelength_unit)

        elif unit in Units.length.keys() and output in Units.frequency.keys():
            self.__frequency_unit = output
            self.__wavelength_unit = unit

            self.__wavelength = Quantity(input, unit=self.__wavelength_unit)
            self.__frequency = EM.compute_frequency(self.__wavelength, unit=self.__wavelength_unit,
                                                    output=self.__frequency_unit)

        else:
            raise UnitError("Input must be a frequency or a wavelength. "
                            "If input is a frequency, unit must be {0}. "
                            "When entering a wavelength, unit must be {1}.".format(str(Units.frequency.keys()),
                                                                                   str(Units.length.keys())))

        # Additional Calculation ---------------------------------------------------------------------------------------
        self.__wavenumber = EM.compute_wavenumber(self.__frequency, output=self.__wavelength_unit)
        self.__region = Bands.which_region(self.__frequency.value, str(self.__frequency_unit))
        self.__band = Bands.which_band(self.__frequency.value, str(self.__frequency_unit))
        self.__array = np.asarray([self.__frequency, self.__wavelength, self.wavenumber])
        self.array = self.__array

    # ------------------------------------------------------------------------------------------------------------------
    # Magic Methods
    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        prefix = '<{0} '.format(self.__class__.__name__)
        sep = ','
        arrstr_freq = np.array2string(self.frequency.value,
                                      separator=sep,
                                      prefix=prefix)

        arrstr_wave = np.array2string(self.wavelength.value,
                                      separator=sep,
                                      prefix=prefix)

        if self.__band is None:
            freq = '{0}{1} Frequency in region {2} in [{3}]>'.format(prefix, arrstr_freq, self.__region,
                                                                     self.__frequency.unitstr)
            wave = '{0}{1} Wavelength in region {2} in [{3}]>'.format(prefix, arrstr_wave, self.__region,
                                                                      self.__wavelength.unitstr)

        else:
            freq = '{0}{1} Frequency in region {2} ({3}-Band) in [{4}]>'.format(prefix, arrstr_freq, self.__region,
                                                                                self.__band,
                                                                                self.__frequency.unitstr)
            wave = '{0}{1} Wavelength in region {2} ({3}-Band) in [{4}]>'.format(prefix, arrstr_wave, self.__region,
                                                                                 self.__band,
                                                                                 self.__wavelength.unitstr)

        return freq + '\n' + wave

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

    @property
    def wavelength(self):
        return self.__wavelength

    @property
    def wavenumber(self):
        return self.__wavenumber

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
            data = tuple(value) + tuple(data, )
        else:
            data = (value,) + tuple(data, )

        data = align_all(data)

        wn = self.wavelength.unit
        wns = '1 / ' + str(wn)

        self.__frequency = Quantity(data[-3], self.frequency.unit)
        self.__wavelength = Quantity(data[-2], self.wavelength.unit)
        self.__wavenumber = Quantity(data[-1], wns)

        return data[0:-3]

    @staticmethod
    def compute_frequency(wavelength, unit, output, quantity=True):
        """
        Convert wavelengths in frequencies.

        Parameters
        ----------
        wavelength : int, float, np.ndarray, respy.units.quantity.Quantity
            Wavelength.
        unit : str, respy.units.Units, sympy.physics.units.quantities.Quantity
            Unit of the wavelength. See respy.units.Units.length.keys() for available units. This is optional
            if the input is an respy.units.quantity.Quantity instance.
        output : str, respy.units.Units, sympy.physics.units.quantities.Quantity
            Unit of entered frequency. See respy.units.Units.frequency.keys() for available units.
        quantity : bool, optional
            If True the output is an respy.units.quantity.Quantity object. If False the output is an array.
            Default is True.

        Returns
        -------
        frequency: float, np.ndarray or respy.units.quantity.Quantity

        """
        if wavelength.__class__.__name__ is 'Quantity':
            wavelength = wavelength.convert_to('m')
        else:
            wavelength = Quantity(wavelength, unit, dtype=np.float)
            wavelength = wavelength.convert_to('m')

        f = const.c / wavelength

        if quantity:
            return f.convert_to(output)
        else:
            f.convert_to(output, True)
            return f.value

    @staticmethod
    def compute_wavelength(frequency, unit, output, quantity=True):
        """
        Convert frequencies in wavelength.

        Parameters
        ----------
        frequency : int, float, np.ndarray, respy.units.quantity.Quantity
            Frequency.
        unit : str, respy.units.Units, sympy.physics.units.quantities.Quantity
            Unit of entered frequency. See respy.units.Units.frequency.keys() for available units. This is optional
            if the input is an respy.units.quantity.Quantity instance.
        output : str, respy.units.Units, sympy.physics.units.quantities.Quantity
            Unit of the wavelength. See respy.units.Units.length.keys() for available units.
        quantity : bool, optional
            If True the output is an respy.units.quantity.Quantity object. If False the output is an array.
            Default is True.
        Returns
        -------
        Wavelength: float, np.ndarray or respy.units.quantity.Quantity
        """
        unit = def_unit(unit)
        output = def_unit(output)

        if frequency.__class__.__name__ == 'Quantity':
            frequency = frequency.convert_to('1 / s')
        else:
            frequency = Quantity(frequency, unit, dtype=np.float)
            frequency = frequency.convert_to('1 / s')

        w = const.c / frequency

        if quantity:
            return w.convert_to(output)
        else:
            w.convert_to(output, True)
            return w.value

    @staticmethod
    def compute_wavenumber(frequency, unit, output, quantity=True):
        """
        Convert frequencies in free space wavenumbers.

        Parameters
        ----------
        frequency : int, float, np.ndarray, respy.units.quantity.Quantity
            Frequency.
        unit : str, respy.units.Units, sympy.physics.units.quantities.Quantity
            Unit of entered frequency. See respy.units.Units.frequency.keys() for available units. This is optional
            if the input is an respy.units.quantity.Quantity instance.
        output : str, respy.units.Units, sympy.physics.units.quantities.Quantity
            Unit of the wavelength. See respy.units.Units.length.keys() for available units.
        quantity : bool, optional
            If True the output is an respy.units.quantity.Quantity object. If False the output is an array.
            Default is True.
        Returns
        -------
        wavenumber: float, np.ndarray or respy.units.quantity.Quantity
        """
        return 2 * const.pi / EM.compute_wavelength(frequency, unit=unit, output=output, quantity=quantity)


class Bands(object):
    def __init__(self, output='GHz', dtype=np.double):
        self.output = def_unit(output)
        self.dimension = self.output.dimension.name
        self.dtype = dtype

        if str(self.dimension) != 'frequency' and str(self.dimension) != 'length':
            raise DimensionError("The output unit must be a dimension of frequency or length.")

    def get_bands(self, bands, quantity=True):
        bands = bands.split()

        band_list = list()
        for item in bands:
            value = self.__get_single_band(item)

            if value.dimension == self.dimension:
                value.convert_to(self.output, True)
                band_list.append(value.value)

            elif str(value.dimension) == 'frequency':
                wavelength = EM.compute_wavelength(value, value.unit, self.output)
                band_list.append(wavelength.value)

            elif str(value.dimension) == 'length':
                frequency = EM.compute_frequency(value, value.unit, self.output)
                band_list.append(frequency.value)

        conc_list = np.concatenate(tuple(band_list))
        conc_list = conc_list.astype(self.dtype)
        conc_list = np.sort(conc_list)

        if quantity:
            return Quantity(conc_list, self.output, dtype=self.dtype)
        else:
            return conc_list

    def get_region(self, region, quantity=True):

        if region == "RADAR" or region == "RADAR".lower():
            return self.get_bands("L S C X", quantity)
        elif region == "OPTICS" or region == "OPTIC" or region == "OPTICS".lower() or region == "OPTIC".lower():
            return self.get_bands("VIS NIR SWIR", quantity)
        elif region == "THERMAL" or region == "TIR" or region == "THERMAL".lower() or region == "TIR".lower():
            return self.get_bands("MWIR LWIR", quantity)
        elif region == "RADIO" or region == "RADIO".lower():
            return self.get_bands("ELF ULF VLF LF MF HF VHF UHF", quantity)
        else:
            raise ValueError(
                "{0} is not a valid region. Supported regions are (lower- or uppercase) {1}".format(str(region),
                                                                                                    str(__REGION__)))

    @staticmethod
    def which_band(value, unit):
        value = Quantity(value, unit)

        for item in __WHICH__BAND__.keys():

            temp_band = __WHICH__BAND__[item]

            if value.dimension == temp_band.dimension:
                temp_band = temp_band.convert_to(value.unit)

            elif str(value.dimension) == 'frequency':
                temp_band = EM.compute_frequency(temp_band, temp_band.unit, value.unit)

            elif str(value.dimension) == 'length':
                temp_band = EM.compute_wavelength(temp_band, temp_band.unit, value.unit)

            else:
                pass

            bands = temp_band[0] <= value <= temp_band[1]

            if np.all(bands):
                return item
            else:
                pass

    @staticmethod
    def which_region(value, unit):
        value = Quantity(value, unit)

        for item in __WHICH__REGION__.keys():

            temp_band = __WHICH__REGION__[item]

            if value.dimension == temp_band.dimension:
                temp_band = temp_band.convert_to(value.unit)

            elif str(value.dimension) == 'frequency':
                temp_band = EM.compute_frequency(temp_band, temp_band.unit, value.unit)

            elif str(value.dimension) == 'length':
                temp_band = EM.compute_wavelength(temp_band, temp_band.unit, value.unit)

            else:
                pass

            bands = temp_band[0] <= value <= temp_band[1]

            if np.all(bands):
                return item
            else:
                pass

    def __get_single_band(self, band):
        if band == "GAMMA" or band == "GAMMA".lower():
            result = np.arange(0, 1.1, 0.1)
            result[0] = 0.0000001
            return Quantity(result[np.argsort(-result)], 'nm', dtype=self.dtype)

        elif band == "XRAY" or band == "XRAY".lower():
            result = np.arange(1.1, 10.1, 1)
            return Quantity(result[np.argsort(-result)], 'nm', dtype=self.dtype)

        elif band == "UV" or band == "UV".lower():
            result = np.arange(10.1, 400, 1)
            return Quantity(result[np.argsort(-result)], 'nm', dtype=self.dtype)

        # ---- Optical Region ----
        elif band == "VIS" or band == "VIS".lower():
            result = np.arange(400., 751., 1)
            return Quantity(result[np.argsort(-result)], 'nm', dtype=self.dtype)

        elif band == "NIR" or band == "NIR".lower():
            result = np.arange(751., 1001., 1)
            return Quantity(result[np.argsort(-result)], 'nm', dtype=self.dtype)

        elif band == "SWIR" or band == "SWIR".lower():
            result = np.arange(1001., 2501., 1)
            return Quantity(result[np.argsort(-result)], 'nm', dtype=self.dtype)

        elif band == "MWIR" or band == "MWIR".lower():
            result = np.arange(3000., 5001., 1)
            return Quantity(result[np.argsort(-result)], 'nm', dtype=self.dtype)

        elif band == "LWIR" or band == "LWIR".lower():
            result = np.arange(8000., 12001., 1)
            return Quantity(result[np.argsort(-result)], 'nm', dtype=self.dtype)

        # ---- Microwave Region ----
        elif band == "L" or band == "L".lower():
            result = np.arange(1, 2.1, 0.1)
            return Quantity(result, 'GHz', dtype=self.dtype)

        elif band == "S" or band == "S".lower():
            result = np.arange(2.1, 4.1, 0.1)
            return Quantity(result, 'GHz', dtype=self.dtype)
        elif band == "C" or band == "C".lower():
            result = np.arange(4.1, 8.1, 0.1)
            return Quantity(result, 'GHz', dtype=self.dtype)
        elif band == "X" or band == "X".lower():
            result = np.arange(8.1, 12.1, 0.1)
            return Quantity(result, 'GHz', dtype=self.dtype)
        elif band == "Ku" or band == "Ku".lower():
            result = np.arange(12.1, 18.1, 0.1)
            return Quantity(result, 'GHz', dtype=self.dtype)
        elif band == "K" or band == "K".lower():
            result = np.arange(18.1, 26.6, 0.1)
            return Quantity(result, 'GHz', dtype=self.dtype)
        elif band == "Ka" or band == "Ka".lower():
            result = np.arange(26.6, 40.1, 0.1)
            return Quantity(result, 'GHz', dtype=self.dtype)
        elif band == "V" or band == "V".lower():
            result = np.arange(50.1, 75.1, 0.1)
            return Quantity(result, 'GHz', dtype=self.dtype)
        elif band == "W" or band == "W".lower():
            result = np.arange(75.1, 110.1, 0.1)
            return Quantity(result, 'GHz', dtype=self.dtype)
        elif band == "D" or band == "D".lower():
            result = np.arange(110.1, 170.1, 0.1)
            return Quantity(result, 'GHz', dtype=self.dtype)

        # ---- Radio Region ----
        elif band == "ELF" or band == "ELF".lower():
            result = np.arange(3, 30.1, 0.1)
            return Quantity(result, 'Hz', dtype=self.dtype)
        elif band == "SLF" or band == "SLF".lower():
            result = np.arange(30.1, 300.1, 0.1)
            return Quantity(result, 'Hz', dtype=self.dtype)
        elif band == "ULF" or band == "ULF".lower():
            result = np.arange(300.1, 3000.1, 0.1)
            return Quantity(result, 'Hz', dtype=self.dtype)
        elif band == "VLF" or band == "VLF".lower():
            result = np.arange(3.1, 30.1, 0.1)
            return Quantity(result, 'kHz', dtype=self.dtype)
        elif band == "LF" or band == "LF".lower():
            result = np.arange(30.1, 300.1, 0.1)
            return Quantity(result, 'kHz', dtype=self.dtype)
        elif band == "MF" or band == "MF".lower():
            result = np.arange(0.31, 3.1, 0.1)
            return Quantity(result, 'MHz', dtype=self.dtype)
        elif band == "HF" or band == "HF".lower():
            result = np.arange(3.1, 30.1, 0.1)
            return Quantity(result, 'MHz', dtype=self.dtype)
        elif band == "VHF" or band == "VHF".lower():
            result = np.arange(30.1, 300.1, 0.1)
            return Quantity(result, 'MHz', dtype=self.dtype)
        else:
            raise ValueError("{0} is not a valid band. "
                             "Supported bands are (lower- or uppercase) {1}.".format(str(band),
                                                                                     str(__BANDS__.keys())))
