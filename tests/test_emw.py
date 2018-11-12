import os
from distutils import dir_util

import pytest
from numpy import loadtxt
from pytest import fixture
import numpy as np
import respy as respy

FREQ_UNIT = ['Hz', 'daHz', 'hHz', 'kHz', 'MHz', 'GHz', 'THz', 'PHz']
WAVE_UNIT = ['nm', 'um', 'mm', 'cm', 'dm', 'm', 'km']


@fixture
def datadir(tmpdir, request):
    """
    Fixture responsible for locating the test data directory and copying it
    into a temporary directory.
    Taken from  http://www.camillescott.org/2016/07/15/travis-pytest-scipyconf/
    """
    filename = request.module.__file__
    test_dir = os.path.dirname(filename)
    data_dir = os.path.join(test_dir, 'data')
    dir_util.copy_tree(data_dir, str(tmpdir))

    def getter(filename, as_str=True):
        filepath = tmpdir.join(filename)
        if as_str:
            return str(filepath)
        return filepath

    return getter


class TestConversion:
    def test_frequency(self, datadir):
        fname = datadir("reference_frequency.csv")

        DATA_ref = loadtxt(fname, unpack=True, skiprows=1, delimiter=',')

        n = 1000
        selection_one = np.random.randint(len(DATA_ref), size=n)
        selection_two = np.random.randint(len(DATA_ref), size=n)

        for i in range(selection_one.shape[0]):
            INPUT = DATA_ref[selection_one[i]]
            INPUT_UNIT = FREQ_UNIT[selection_one[i]]

            REF = DATA_ref[selection_two[i]]
            REF_UNIT = FREQ_UNIT[selection_two[i]]

            TEST_REF = respy.convert_frequency(frequency=INPUT, unit=INPUT_UNIT, output=REF_UNIT)
            TEST_INPUT = respy.convert_frequency(frequency=TEST_REF, unit=REF_UNIT, output=INPUT_UNIT)

            for j in range(TEST_REF.shape[0]):
                assert np.allclose(REF[j], TEST_REF[j])
                assert np.allclose(INPUT[j], TEST_INPUT[j])

    def test_wavelength(self, datadir):
        WAVE_UNIT = ['nm', 'mm', 'cm', 'dm', 'm', 'km']

        fname = datadir("reference_lengths.csv")

        DATA_ref = loadtxt(fname, unpack=True, skiprows=1, delimiter=';')

        n = 1000
        selection_one = np.random.randint(len(DATA_ref), size=n)
        selection_two = np.random.randint(len(DATA_ref), size=n)

        for i in range(selection_one.shape[0]):
            INPUT = DATA_ref[selection_one[i]]
            INPUT_UNIT = WAVE_UNIT[selection_one[i]]

            REF = DATA_ref[selection_two[i]]
            REF_UNIT = WAVE_UNIT[selection_two[i]]

            TEST_REF = respy.convert_wavelength(wavelength=INPUT, unit=INPUT_UNIT, output=REF_UNIT)
            TEST_INPUT = respy.convert_wavelength(wavelength=TEST_REF, unit=REF_UNIT, output=INPUT_UNIT)

            for j in range(TEST_REF.shape[0]):
                assert np.allclose(REF[j], TEST_REF[j])
                assert np.allclose(INPUT[j], TEST_INPUT[j])

    def test_freq_to_wave(self, datadir):
        WAVE_UNIT = ['mm', 'cm', 'm', 'km']
        FREQ_UNIT = ['Hz', 'kHz', 'MHz', 'GHz']

        fname = datadir("reference_freq_to_wave.csv")

        Hz, mm, Khz, cm, MHz, m, GHz, km = loadtxt(fname, unpack=True, skiprows=1, delimiter=';')

        DATA_HZ = zip(Hz, mm)
        DATA_Khz = zip(Khz, cm)
        DATA_MHz = zip(MHz, m)
        DATA_GHz = zip(GHz, km)

        DATA_REF = (DATA_HZ, DATA_Khz, DATA_MHz, DATA_GHz)
        n = len(DATA_HZ)

        for i in range(len(DATA_REF)):
            for j in range(n):
                freqcuency_ref = DATA_REF[i][j][0]
                wavelength_ref = DATA_REF[i][j][1]

                freqcuency_ref_unit = FREQ_UNIT[i]
                wavelength_ref_unit = WAVE_UNIT[i]

                wavelength = respy.compute_wavelength(frequency=freqcuency_ref, unit=freqcuency_ref_unit,
                                                      output=wavelength_ref_unit)

                frequency = respy.compute_frequency(wavelength=wavelength, unit=wavelength_ref_unit,
                                                    output=freqcuency_ref_unit)

                assert np.allclose(wavelength_ref, wavelength)
                assert np.allclose(freqcuency_ref, frequency)


class TestRaises:
    def test_which_band_raise(self):
        with pytest.raises(ValueError):
            respy.which_band(1.26, unit='XXX')


@pytest.mark.webtest
@pytest.mark.parametrize(
    "frequency, band,", [
        (1.26, 'L'),
        (10, 'X',),
        (5.26, 'C'),
        (28, 'Ka'),
        (65, 'V'),
        (100, 'W'),
        (150, 'D'),
        (15000, 'NONE')
    ])
class TestSelectionRADAR:
    def test_which_band(self, frequency, band):
        band_selected = respy.which_band(frequency)
        wavelength = respy.compute_wavelength(frequency=frequency)
        band_selected_with_wavelength = respy.which_band(wavelength, unit='cm')

        assert band_selected == band
        assert band_selected_with_wavelength == band

    def test_which_band_array(self, frequency, band):
        frequency = np.array([1.26, 10, 5.26, 28, 65, 100, 150, 15000])
        band = 'LXCKVWD'
        band = list(band)

        for i in range(len(band)):
            item = band[i]

            if item is 'K':
                band[i] = item + 'a'
            elif item is 'a':
                del band[i]
            else:
                pass

        band_selected = respy.which_band(frequency)
        wavelength = respy.compute_wavelength(frequency=frequency)
        band_selected_with_wavelength = respy.which_band(wavelength, unit='cm')

        assert len(band_selected) == len(band)
        assert len(band_selected_with_wavelength) == len(band)

        for i in range(len(band_selected)):
            assert band_selected[i] in band
            assert band_selected_with_wavelength[i] in band


@pytest.mark.webtest
@pytest.mark.parametrize(
    "wavelength, band,", [
        (500, 'VIS'),
        (1500, 'SWIR',),
        (700, 'VIS'),
        (800, 'NIR'),
        (950, 'NIR'),
        (2456, 'SWIR'),
        (1010, 'SWIR'),
        (10000, 'LWIR'),
        (5000, 'MWIR')
    ])
class TestSelectionOPTIC:
    def test_which_band(self, wavelength, band):
        band_selected = respy.which_band(wavelength, 'nm')
        frequency = respy.compute_frequency(wavelength=wavelength, unit='nm')
        band_selected_with_frequency = respy.which_band(frequency, 'GHz')

        assert band_selected == band
        assert band_selected_with_frequency == band

    def test_which_band_array(self, wavelength, band):
        DATA = ((500, 'VIS'),
                (1500, 'SWIR',),
                (700, 'VIS'),
                (800, 'NIR'),
                (950, 'NIR'),
                (2456, 'SWIR'),
                (1010, 'SWIR'),
                (10000, 'LWIR'),
                (5000, 'MWIR'))

        band = [DATA[i][1] for i in range(len(DATA))]
        wavelength = np.asarray([DATA[i][0] for i in range(len(DATA))])
        unique_bands = set(band)

        band_selected = respy.which_band(wavelength, 'nm')
        frequency = respy.compute_frequency(wavelength=wavelength, unit='nm')
        band_selected_with_frequency = respy.which_band(frequency, 'GHz')

        assert len(band_selected) == len(unique_bands)
        assert len(band_selected_with_frequency) == len(unique_bands)

        for i in range(len(band_selected)):
            assert band_selected[i] in unique_bands
            assert band_selected_with_frequency[i] in unique_bands


class TestSelectBand:
    BANDS = ["VIS", "NIR", "SWIR", "MWIR", "LWIR", "L", "S", "C", "X", "Ku", "K", "Ka", "V", "W", "D"]
    pass
