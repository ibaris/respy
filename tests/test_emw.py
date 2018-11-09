import radarpy as respy
import numpy as np
import pytest


@pytest.mark.webtest
@pytest.mark.parametrize(
    "frequency, band,", [
        (1.26, 'L'),
        (10, 'X',),
        (5.26, 'C'),
        (28, 'Ka'),
        (65, 'V'),
        (100, 'W'),
        (150, 'D')
    ])
class TestSelectionRADAR:
    def test_which_band(self, frequency, band):
        band_selected = respy.which_band(frequency)

        assert band_selected == band


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

        assert band_selected == band
