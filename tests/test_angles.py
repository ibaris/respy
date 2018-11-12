from __future__ import division

import numpy as np
import pytest
from numpy import allclose

from respy import Angles
import sys
# python 3.6 comparability
if sys.version_info < (3, 0):
   n = 12
else:
    n = 17


DTYPES = [np.bool, np.byte, np.ubyte, np.short, np.ushort, np.intc, np.uintc, np.int_, np.uint, np.longlong,
          np.ulonglong, np.half, np.float, np.float16, np.single, np.double, np.longdouble, np.csingle, np.cdouble,
          np.clongdouble, np.int, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64,
          np.intp,
          np.uintp, np.float32, np.float64, np.complex, np.complex64, np.complex128, float, int, complex]


# Test Raise Exceptions ------------------------------------------------------------------------------------------------
class TestRaises:
    def test_raa_raise(self):
        with pytest.raises(ValueError):
            angles = Angles(iza=10, vza=30)

    def test_angle_unit_raise(self):
        with pytest.raises(ValueError):
            anlges = Angles(iza=10, vza=10, raa=10, angle_unit='XXX')

    def test_normalize_raise(self):
        angles = Angles(iza=10, vza=10, raa=10)
        with pytest.raises(TypeError):
            angles.normalize = 3

    def test_raa_iaa_vaa_defined_raise(self):
        with pytest.raises(AssertionError):
            anlges = Angles(iza=10, vza=10, raa=10, iaa=10, vaa=10)

    def test_dtype_raise(self):
        with pytest.raises(TypeError):
            anlges = Angles(iza=10, vza=10, raa=10, dtype='XXX')

    def test_dtype_raise_setter(self):
        angles = Angles(iza=10, vza=10, raa=10)
        with pytest.raises(TypeError):
            angles.dtype = 'XXX'

    def test_len_assertion_raise(self):
        with pytest.raises(AssertionError):
            anlges = Angles(iza=np.array([10, 20]).flatten(), vza=10, raa=10, align=False)

    def test_no_raise_at_RADDEG(self):
        angles = Angles(iza=10, vza=10, raa=10, angle_unit='RAD')
        angles = Angles(iza=10, vza=10, raa=10, angle_unit='rad')
        angles = Angles(iza=10, vza=10, raa=10, angle_unit='DEG')
        angles = Angles(iza=10, vza=10, raa=10, angle_unit='deg')


class TestSpecials:
    def test__str__(self):
        angles = Angles(iza=10, vza=20, iaa=30, vaa=12, alpha=45, beta=66)
        n = 17

        str_output = angles.__str__().split()

        assert str_output[10][0:-1] == str(round(np.deg2rad(10), n))
        assert str_output[11] == str(10.0)
        assert str_output[19][0:-1] == str(round(np.deg2rad(20), n))
        assert str_output[20] == str(20.0)
        assert str_output[28][0:-1] == str(round(np.deg2rad(30 - 12), n))
        assert str_output[29] == str(30.0 - 12.0)
        assert str_output[37][0:-1] == str(round(np.deg2rad(30), n))
        assert str_output[38] == str(30.0)
        assert str_output[46][0:-1] == str(round(np.deg2rad(12), n))
        assert str_output[47] == str(12.0)
        assert str_output[54][0:-1] == str(round(np.deg2rad(45), n))
        assert str_output[55] == str(45.0)
        assert str_output[62][0:-1] == str(round(np.deg2rad(66), n))
        assert str_output[63] == str(66.0)
        assert str_output[69][0:-1] == str(round(angles.B[0], 11))
        assert str_output[70] == str(round(angles.BDeg[0], 11))

        angles.normalize = True

        str_output = angles.__str__().split()

        assert str_output[10][0:-1] == str(round(np.deg2rad(10), n))
        assert str_output[11] == str(10.0)
        assert str_output[19][0:-1] == str(round(np.deg2rad(20), n))
        assert str_output[20] == str(20.0)
        assert str_output[28][0:-1] == str(round(np.deg2rad(30 - 12), n))
        assert str_output[29] == str(30.0 - 12.0)
        assert str_output[37][0:-1] == str(round(np.deg2rad(30), n))
        assert str_output[38] == str(30.0)
        assert str_output[46][0:-1] == str(round(np.deg2rad(12), n))
        assert str_output[47] == str(12.0)
        assert str_output[54][0:-1] == str(round(np.deg2rad(45), n))
        assert str_output[55] == str(45.0)
        assert str_output[62][0:-1] == str(round(np.deg2rad(66), n))
        assert str_output[63] == str(66.0)
        assert str_output[69][0:-1] == str(round(angles.B[0], 11))
        assert str_output[70] == str(round(angles.BDeg[0], 11))

    def test__len__(self):
        angles = Angles(iza=10, vza=10, raa=10, alpha=10, beta=10, normalize=True)
        assert angles.shape == (7, 2)
        assert len(angles) == 7

    def test__repr__(self):
        angles = Angles(iza=10, vza=20, iaa=30, vaa=12, alpha=45, beta=66)
        repr_string = angles.__repr__()
        ref = "Angles(iza=[10.], vza=[20.], raa=[18.], iaa=[30.], vaa=[12.], alpha=[45.], beta=[66.], normalize=False, nbar=0.0, angle_unit=DEG, align=True, dtype=<type 'numpy.float64'>)"

        assert angles.__repr__() == angles.__repr__()


@pytest.mark.webtest
@pytest.mark.parametrize(
    "izaDegSingle, vzaDegSingle, raaDegSingle, iaaDegSingle, vaaDegSingle, alphaDegSingle, betaDegSingle", [
        tuple(np.linspace(0, 10, 7).tolist()),
        tuple(np.linspace(10, 20, 7).tolist()),
        tuple(np.linspace(20, 30, 7).tolist()),
        tuple(np.linspace(30, 40, 7).tolist()),
        tuple(np.linspace(40, 50, 7).tolist()),
        tuple(np.linspace(50, 60, 7).tolist()),
        tuple(np.linspace(60, 70, 7).tolist()),
        tuple(np.linspace(70, 80, 7).tolist()),
        tuple(np.linspace(80, 90, 7).tolist()),
        tuple(np.linspace(90, 100, 7).tolist()),
        tuple(np.linspace(100, 110, 7).tolist()),
        tuple(np.linspace(110, 120, 7).tolist()),
        tuple(np.linspace(120, 130, 7).tolist()),
        tuple(np.linspace(130, 140, 7).tolist()),
        tuple(np.linspace(140, 150, 7).tolist()),
        tuple(np.linspace(150, 160, 7).tolist()),
        tuple(np.linspace(160, 170, 7).tolist()),
        tuple(np.linspace(170, 180, 7).tolist()),
        tuple(np.linspace(180, 190, 7).tolist()),
    ])
class TestAngleConversionDEG:
    def test_deg2rad_raa(self, izaDegSingle, vzaDegSingle, raaDegSingle, iaaDegSingle, vaaDegSingle, alphaDegSingle,
                         betaDegSingle):
        izaRadSingle, vzaRadSingle, raaRadSingle, alphaRadSingle, betaRadSingle = (np.deg2rad(izaDegSingle),
                                                                                   np.deg2rad(vzaDegSingle),
                                                                                   np.deg2rad(raaDegSingle),
                                                                                   np.deg2rad(alphaDegSingle),
                                                                                   np.deg2rad(betaDegSingle))

        mui, muv = np.cos(izaRadSingle), np.cos(vzaRadSingle)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegSingle) + 1 / np.cos(vzaDegSingle)

        angles = Angles(iza=izaDegSingle, vza=vzaDegSingle, raa=raaDegSingle, alpha=alphaDegSingle, beta=betaDegSingle)

        assert allclose(angles.iza, izaRadSingle)
        assert allclose(angles.vza, vzaRadSingle)
        assert allclose(angles.raa, raaRadSingle)
        assert allclose(angles.iaa, 0)
        assert allclose(angles.vaa, 0)
        assert allclose(angles.alpha, alphaRadSingle)
        assert allclose(angles.beta, betaRadSingle)
        assert angles.phi == angles.raa

        assert allclose(angles.izaDeg, izaDegSingle)
        assert allclose(angles.vzaDeg, vzaDegSingle)
        assert allclose(angles.raaDeg, raaDegSingle)
        assert allclose(angles.iaaDeg, 0)
        assert allclose(angles.vaaDeg, 0)
        assert allclose(angles.alphaDeg, alphaDegSingle)
        assert allclose(angles.betaDeg, betaDegSingle)

        assert allclose(angles.mui, mui)
        assert allclose(angles.muv, muv)
        assert allclose(angles.B, B)
        assert allclose(angles.BDeg, BDeg)

        for i in range(7):
            assert angles.array[i] == angles.geometries[0][i]

        for i in range(7):
            assert angles.arrayDeg[i] == angles.geometriesDeg[0][i]

    def test_deg2rad_iaa_vaa(self, izaDegSingle, vzaDegSingle, raaDegSingle, iaaDegSingle, vaaDegSingle,
                             alphaDegSingle, betaDegSingle):
        izaRadSingle, vzaRadSingle, iaaRadSingle, vaaRadSingle, alphaRadSingle, betaRadSingle = (
            np.deg2rad(izaDegSingle), np.deg2rad(vzaDegSingle),
            np.deg2rad(iaaDegSingle), np.deg2rad(vaaDegSingle), np.deg2rad(alphaDegSingle), np.deg2rad(betaDegSingle))

        mui, muv = np.cos(izaRadSingle), np.cos(vzaRadSingle)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegSingle) + 1 / np.cos(vzaDegSingle)

        angles = Angles(iza=izaDegSingle, vza=vzaDegSingle, iaa=iaaDegSingle, vaa=vaaDegSingle, alpha=alphaDegSingle,
                        beta=betaDegSingle)

        assert allclose(angles.iza, izaRadSingle)
        assert allclose(angles.vza, vzaRadSingle)
        assert allclose(angles.iaa, iaaRadSingle)
        assert allclose(angles.vaa, vaaRadSingle)
        assert allclose(angles.raa, iaaRadSingle - vaaRadSingle)
        assert allclose(angles.alpha, alphaRadSingle)
        assert allclose(angles.beta, betaRadSingle)

        assert allclose(angles.izaDeg, izaDegSingle)
        assert allclose(angles.vzaDeg, vzaDegSingle)
        assert allclose(angles.iaaDeg, iaaDegSingle)
        assert allclose(angles.vaaDeg, vaaDegSingle)
        assert allclose(angles.raaDeg, iaaDegSingle - vaaDegSingle)
        assert allclose(angles.alphaDeg, alphaDegSingle)
        assert allclose(angles.betaDeg, betaDegSingle)

        assert allclose(angles.mui, mui)
        assert allclose(angles.muv, muv)
        assert allclose(angles.B, B)
        assert allclose(angles.BDeg, BDeg)

        for i in range(7):
            assert angles.array[i] == angles.geometries[0][i]

        for i in range(7):
            assert angles.arrayDeg[i] == angles.geometriesDeg[0][i]


@pytest.mark.webtest
@pytest.mark.parametrize(
    "izaRadSingle, vzaRadSingle, raaRadSingle, iaaRadSingle, vaaRadSingle, alphaRadSingle, betaRadSingle", [
        tuple(np.linspace(0, .1, 7).tolist()),
        tuple(np.linspace(1, .2, 7).tolist()),
        tuple(np.linspace(2, .3, 7).tolist()),
        tuple(np.linspace(3, .4, 7).tolist()),
        tuple(np.linspace(4, .5, 7).tolist()),
        tuple(np.linspace(5, .6, 7).tolist()),
        tuple(np.linspace(6, .7, 7).tolist()),
        tuple(np.linspace(.70, .80, 7).tolist()),
        tuple(np.linspace(.80, .90, 7).tolist()),
        tuple(np.linspace(.90, 1.00, 7).tolist()),
        tuple(np.linspace(1.00, 1.10, 7).tolist()),
        tuple(np.linspace(1.10, 1.20, 7).tolist()),
        tuple(np.linspace(1.20, 1.30, 7).tolist()),
        tuple(np.linspace(1.30, 1.40, 7).tolist()),
        tuple(np.linspace(1.40, 1.50, 7).tolist()),
        tuple(np.linspace(1.50, 1.60, 7).tolist()),
        tuple(np.linspace(1.60, 1.70, 7).tolist()),
        tuple(np.linspace(1.70, 1.80, 7).tolist()),
        tuple(np.linspace(1.90, 1.90, 7).tolist()),
        tuple(np.linspace(2.00, 2.10, 7).tolist()),
        tuple(np.linspace(2.10, 2.20, 7).tolist()),
        tuple(np.linspace(2.20, 2.30, 7).tolist()),
        tuple(np.linspace(2.30, 2.40, 7).tolist()),
        tuple(np.linspace(2.40, 2.50, 7).tolist()),
        tuple(np.linspace(2.50, 2.60, 7).tolist()),
        tuple(np.linspace(2.60, 2.70, 7).tolist()),
        tuple(np.linspace(2.70, 2.80, 7).tolist()),
        tuple(np.linspace(2.80, 2.90, 7).tolist()),
        tuple(np.linspace(2.90, 3.00, 7).tolist()),
        tuple(np.linspace(3.00, 3.10, 7).tolist()),
        tuple(np.linspace(3.10, 3.20, 7).tolist()),
    ])
class TestAngleConversionRAD:
    def test_deg2rad_raa(self, izaRadSingle, vzaRadSingle, raaRadSingle, iaaRadSingle, vaaRadSingle, alphaRadSingle,
                         betaRadSingle):
        izaDegSingle, vzaDegSingle, raaDegSingle, alphaDegSingle, betaDegSingle = (np.rad2deg(izaRadSingle),
                                                                                   np.rad2deg(vzaRadSingle),
                                                                                   np.rad2deg(raaRadSingle),
                                                                                   np.rad2deg(alphaRadSingle),
                                                                                   np.rad2deg(betaRadSingle))

        mui, muv = np.cos(izaRadSingle), np.cos(vzaRadSingle)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegSingle) + 1 / np.cos(vzaDegSingle)

        angles = Angles(iza=izaRadSingle, vza=vzaRadSingle, raa=raaRadSingle, alpha=alphaRadSingle, beta=betaRadSingle,
                        angle_unit='RAD')

        assert allclose(angles.iza, izaRadSingle)
        assert allclose(angles.vza, vzaRadSingle)
        assert allclose(angles.raa, raaRadSingle)
        assert allclose(angles.iaa, 0)
        assert allclose(angles.vaa, 0)
        assert allclose(angles.alpha, alphaRadSingle)
        assert allclose(angles.beta, betaRadSingle)

        assert allclose(angles.izaDeg, izaDegSingle)
        assert allclose(angles.vzaDeg, vzaDegSingle)
        assert allclose(angles.raaDeg, raaDegSingle)
        assert allclose(angles.iaaDeg, 0)
        assert allclose(angles.vaaDeg, 0)
        assert allclose(angles.alphaDeg, alphaDegSingle)
        assert allclose(angles.betaDeg, betaDegSingle)

        assert allclose(angles.mui, mui)
        assert allclose(angles.muv, muv)
        assert allclose(angles.B, B)
        assert allclose(angles.BDeg, BDeg)

    def test_deg2rad_iaa_vaa(self, izaRadSingle, vzaRadSingle, raaRadSingle, iaaRadSingle, vaaRadSingle,
                             alphaRadSingle, betaRadSingle):
        izaDegSingle, vzaDegSingle, iaaDegSingle, vaaDegSingle, alphaDegSingle, betaDegSingle = (
            np.rad2deg(izaRadSingle), np.rad2deg(vzaRadSingle),
            np.rad2deg(iaaRadSingle), np.rad2deg(vaaRadSingle), np.rad2deg(alphaRadSingle), np.rad2deg(betaRadSingle))

        mui, muv = np.cos(izaRadSingle), np.cos(vzaRadSingle)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegSingle) + 1 / np.cos(vzaDegSingle)

        angles = Angles(iza=izaRadSingle, vza=vzaRadSingle, iaa=iaaRadSingle, vaa=vaaRadSingle, alpha=alphaRadSingle,
                        beta=betaRadSingle, angle_unit='RAD')

        assert allclose(angles.iza, izaRadSingle)
        assert allclose(angles.vza, vzaRadSingle)
        assert allclose(angles.iaa, iaaRadSingle)
        assert allclose(angles.vaa, vaaRadSingle)
        assert allclose(angles.raa, iaaRadSingle - vaaRadSingle)
        assert allclose(angles.alpha, alphaRadSingle)
        assert allclose(angles.beta, betaRadSingle)

        assert allclose(angles.izaDeg, izaDegSingle)
        assert allclose(angles.vzaDeg, vzaDegSingle)
        assert allclose(angles.iaaDeg, iaaDegSingle)
        assert allclose(angles.vaaDeg, vaaDegSingle)
        assert allclose(angles.raaDeg, iaaDegSingle - vaaDegSingle)
        assert allclose(angles.alphaDeg, alphaDegSingle)
        assert allclose(angles.betaDeg, betaDegSingle)

        assert allclose(angles.mui, mui)
        assert allclose(angles.muv, muv)
        assert allclose(angles.B, B)
        assert allclose(angles.BDeg, BDeg)


izaDegArray, vzaDegArray, raaDegArray, iaaDegArray, vaaDegArray, alphaDegArray, betaDegArray = (
    np.arange(0, 10, 1), np.arange(10, 20, 1), np.arange(20, 30, 1), np.arange(30, 40, 1), np.arange(40, 50, 1),
    np.arange(50, 60, 1), np.arange(60, 70, 1))


@pytest.mark.webtest
@pytest.mark.parametrize(
    "izaDegArray, vzaDegArray, raaDegArray, iaaDegArray, vaaDegArray, alphaDegArray, betaDegArray", [
        (np.arange(0, 10, 1), np.arange(10, 20, 1), np.arange(20, 30, 1), np.arange(30, 40, 1), np.arange(40, 50, 1),
         np.arange(50, 60, 1), np.arange(60, 70, 1)),
        (np.arange(10, 20, 1), np.arange(20, 30, 1), np.arange(30, 40, 1), np.arange(40, 50, 1), np.arange(50, 60, 1),
         np.arange(60, 70, 1), np.arange(70, 80, 1)),
        (np.arange(20, 30, 1), np.arange(30, 40, 1), np.arange(40, 50, 1), np.arange(50, 60, 1), np.arange(60, 70, 1),
         np.arange(70, 80, 1), np.arange(80, 90, 1)),
        (np.arange(30, 40, 1), np.arange(40, 50, 1), np.arange(50, 60, 1), np.arange(60, 70, 1), np.arange(70, 80, 1),
         np.arange(80, 90, 1), np.arange(90, 100, 1)),
        (np.arange(40, 50, 1), np.arange(50, 60, 1), np.arange(60, 70, 1), np.arange(70, 80, 1), np.arange(80, 90, 1),
         np.arange(90, 100, 1), np.arange(100, 110, 1)),
        (np.arange(50, 60, 1), np.arange(60, 70, 1), np.arange(70, 80, 1), np.arange(80, 90, 1), np.arange(90, 100, 1),
         np.arange(100, 110, 1), np.arange(110, 120, 1)),
        (
                np.arange(60, 70, 1), np.arange(70, 80, 1), np.arange(80, 90, 1), np.arange(90, 100, 1),
                np.arange(100, 110, 1),
                np.arange(110, 120, 1), np.arange(120, 130, 1)),

    ])
class TestAngleConversionArrayDEG:
    def test_deg2rad_raa(self, izaDegArray, vzaDegArray, raaDegArray, iaaDegArray, vaaDegArray, alphaDegArray,
                         betaDegArray):
        izaRadArray, vzaRadArray, raaRadArray, alphaRadArray, betaRadArray = (np.deg2rad(izaDegArray),
                                                                              np.deg2rad(vzaDegArray),
                                                                              np.deg2rad(raaDegArray),
                                                                              np.deg2rad(alphaDegArray),
                                                                              np.deg2rad(betaDegArray))

        mui, muv = np.cos(izaRadArray), np.cos(vzaRadArray)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegArray) + 1 / np.cos(vzaDegArray)

        angles = Angles(iza=izaDegArray, vza=vzaDegArray, raa=raaDegArray, alpha=alphaDegArray, beta=betaDegArray)

        assert allclose(angles.iza, izaRadArray)
        assert allclose(angles.vza, vzaRadArray)
        assert allclose(angles.raa, raaRadArray)
        assert allclose(angles.iaa, 0)
        assert allclose(angles.vaa, 0)
        assert allclose(angles.alpha, alphaRadArray)
        assert allclose(angles.beta, betaRadArray)

        assert allclose(angles.izaDeg, izaDegArray)
        assert allclose(angles.vzaDeg, vzaDegArray)
        assert allclose(angles.raaDeg, raaDegArray)
        assert allclose(angles.iaaDeg, 0)
        assert allclose(angles.vaaDeg, 0)
        assert allclose(angles.alphaDeg, alphaDegArray)
        assert allclose(angles.betaDeg, betaDegArray)

        assert allclose(angles.mui, mui)
        assert allclose(angles.muv, muv)
        assert allclose(angles.B, B)
        assert allclose(angles.BDeg, BDeg)

        assert allclose(angles.shape[1], izaDegArray.shape[0])

        for i in range(angles.shape[1]):
            for j in range(angles.shape[0]):
                item = angles.array[j, i]

                assert item == angles.geometries[i][j]

        for i in range(angles.shape[1]):
            for j in range(angles.shape[0]):
                item = angles.arrayDeg[j, i]

                assert item == angles.geometriesDeg[i][j]

    def test_deg2rad_iaa_vaa(self, izaDegArray, vzaDegArray, raaDegArray, iaaDegArray, vaaDegArray,
                             alphaDegArray, betaDegArray):
        izaRadArray, vzaRadArray, iaaRadArray, vaaRadArray, alphaRadArray, betaRadArray = (
            np.deg2rad(izaDegArray), np.deg2rad(vzaDegArray),
            np.deg2rad(iaaDegArray), np.deg2rad(vaaDegArray), np.deg2rad(alphaDegArray), np.deg2rad(betaDegArray))

        mui, muv = np.cos(izaRadArray), np.cos(vzaRadArray)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegArray) + 1 / np.cos(vzaDegArray)

        angles = Angles(iza=izaDegArray, vza=vzaDegArray, iaa=iaaDegArray, vaa=vaaDegArray, alpha=alphaDegArray,
                        beta=betaDegArray)

        assert allclose(angles.iza, izaRadArray)
        assert allclose(angles.vza, vzaRadArray)
        assert allclose(angles.iaa, iaaRadArray)
        assert allclose(angles.vaa, vaaRadArray)
        assert allclose(angles.raa, iaaRadArray - vaaRadArray)
        assert allclose(angles.alpha, alphaRadArray)
        assert allclose(angles.beta, betaRadArray)

        assert allclose(angles.izaDeg, izaDegArray)
        assert allclose(angles.vzaDeg, vzaDegArray)
        assert allclose(angles.iaaDeg, iaaDegArray)
        assert allclose(angles.vaaDeg, vaaDegArray)
        assert allclose(angles.raaDeg, iaaDegArray - vaaDegArray)
        assert allclose(angles.alphaDeg, alphaDegArray)
        assert allclose(angles.betaDeg, betaDegArray)

        assert allclose(angles.mui, mui)
        assert allclose(angles.muv, muv)
        assert allclose(angles.B, B)
        assert allclose(angles.BDeg, BDeg)

        assert allclose(angles.shape[1], izaDegArray.shape[0])

        for i in range(angles.shape[1]):
            for j in range(angles.shape[0]):
                item = angles.array[j, i]

                assert item == angles.geometries[i][j]

        for i in range(angles.shape[1]):
            for j in range(angles.shape[0]):
                item = angles.arrayDeg[j, i]

                assert item == angles.geometriesDeg[i][j]


@pytest.mark.webtest
@pytest.mark.parametrize(
    "izaRadArray, vzaRadArray, raaRadArray, iaaRadArray, vaaRadArray, alphaRadArray, betaRadArray", [
        (np.arange(0, 10, 1), np.arange(10, 20, 1), np.arange(20, 30, 1), np.arange(30, 40, 1), np.arange(40, 50, 1),
         np.arange(50, 60, 1), np.arange(60, 70, 1)),
        (np.arange(10, 20, 1), np.arange(20, 30, 1), np.arange(30, 40, 1), np.arange(40, 50, 1), np.arange(50, 60, 1),
         np.arange(60, 70, 1), np.arange(70, 80, 1)),
        (np.arange(20, 30, 1), np.arange(30, 40, 1), np.arange(40, 50, 1), np.arange(50, 60, 1), np.arange(60, 70, 1),
         np.arange(70, 80, 1), np.arange(80, 90, 1)),
        (np.arange(30, 40, 1), np.arange(40, 50, 1), np.arange(50, 60, 1), np.arange(60, 70, 1), np.arange(70, 80, 1),
         np.arange(80, 90, 1), np.arange(90, 100, 1)),
        (np.arange(40, 50, 1), np.arange(50, 60, 1), np.arange(60, 70, 1), np.arange(70, 80, 1), np.arange(80, 90, 1),
         np.arange(90, 100, 1), np.arange(100, 110, 1)),
        (np.arange(50, 60, 1), np.arange(60, 70, 1), np.arange(70, 80, 1), np.arange(80, 90, 1), np.arange(90, 100, 1),
         np.arange(100, 110, 1), np.arange(110, 120, 1)),
        (
                np.arange(60, 70, 1), np.arange(70, 80, 1), np.arange(80, 90, 1), np.arange(90, 100, 1),
                np.arange(100, 110, 1),
                np.arange(110, 120, 1), np.arange(120, 130, 1)),

    ])
class TestAngleConversionArrayRad:
    def test_Rad2rad_raa(self, izaRadArray, vzaRadArray, raaRadArray, iaaRadArray, vaaRadArray, alphaRadArray,
                         betaRadArray):
        izaDegArray, vzaDegArray, raaDegArray, alphaDegArray, betaDegArray = (np.rad2deg(izaRadArray / 100.),
                                                                              np.rad2deg(vzaRadArray / 100.),
                                                                              np.rad2deg(raaRadArray / 100.),
                                                                              np.rad2deg(alphaRadArray / 100.),
                                                                              np.rad2deg(betaRadArray / 100.))

        mui, muv = np.cos(izaRadArray / 100), np.cos(vzaRadArray / 100)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegArray) + 1 / np.cos(vzaDegArray)

        angles = Angles(iza=izaRadArray / 100., vza=vzaRadArray / 100., raa=raaRadArray / 100.,
                        alpha=alphaRadArray / 100.,
                        beta=betaRadArray / 100.,
                        angle_unit='RAD')

        assert allclose(angles.iza, izaRadArray / 100)
        assert allclose(angles.vza, vzaRadArray / 100)
        assert allclose(angles.raa, raaRadArray / 100)
        assert allclose(angles.iaa, 0)
        assert allclose(angles.vaa, 0)
        assert allclose(angles.alpha, alphaRadArray / 100)
        assert allclose(angles.beta, betaRadArray / 100)

        assert allclose(angles.izaDeg, izaDegArray)
        assert allclose(angles.vzaDeg, vzaDegArray)
        assert allclose(angles.raaDeg, raaDegArray)
        assert allclose(angles.iaaDeg, 0)
        assert allclose(angles.vaaDeg, 0)
        assert allclose(angles.alphaDeg, alphaDegArray)
        assert allclose(angles.betaDeg, betaDegArray)

        assert allclose(angles.mui, mui)
        assert allclose(angles.muv, muv)
        assert allclose(angles.B, B)
        assert allclose(angles.BDeg, BDeg)

        assert allclose(angles.shape[1], izaDegArray.shape[0])

        for i in range(angles.shape[1]):
            for j in range(angles.shape[0]):
                item = angles.array[j, i]

                assert item == angles.geometries[i][j]

        for i in range(angles.shape[1]):
            for j in range(angles.shape[0]):
                item = angles.arrayDeg[j, i]

                assert item == angles.geometriesDeg[i][j]

    def test_Rad2rad_iaa_vaa(self, izaRadArray, vzaRadArray, raaRadArray, iaaRadArray, vaaRadArray,
                             alphaRadArray, betaRadArray):
        izaDegArray, vzaDegArray, iaaDegArray, vaaDegArray, alphaDegArray, betaDegArray = (
            np.rad2deg(izaRadArray / 100.), np.rad2deg(vzaRadArray / 100.),
            np.rad2deg(iaaRadArray / 100.), np.rad2deg(vaaRadArray / 100.), np.rad2deg(alphaRadArray / 100.),
            np.rad2deg(betaRadArray / 100.))

        mui, muv = np.cos(izaRadArray / 100), np.cos(vzaRadArray / 100)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegArray) + 1 / np.cos(vzaDegArray)

        angles = Angles(iza=izaRadArray / 100., vza=vzaRadArray / 100., iaa=iaaRadArray / 100., vaa=vaaRadArray / 100.,
                        alpha=alphaRadArray / 100.,
                        beta=betaRadArray / 100., angle_unit='RAD')

        assert allclose(angles.iza, izaRadArray / 100)
        assert allclose(angles.vza, vzaRadArray / 100)
        assert allclose(angles.iaa, iaaRadArray / 100)
        assert allclose(angles.vaa, vaaRadArray / 100)
        assert allclose(angles.raa, iaaRadArray / 100 - vaaRadArray / 100)
        assert allclose(angles.alpha, alphaRadArray / 100)
        assert allclose(angles.beta, betaRadArray / 100)

        assert allclose(angles.izaDeg, izaDegArray)
        assert allclose(angles.vzaDeg, vzaDegArray)
        assert allclose(angles.iaaDeg, iaaDegArray)
        assert allclose(angles.vaaDeg, vaaDegArray)
        assert allclose(angles.raaDeg, iaaDegArray - vaaDegArray)
        assert allclose(angles.alphaDeg, alphaDegArray)
        assert allclose(angles.betaDeg, betaDegArray)

        assert allclose(angles.mui, mui)
        assert allclose(angles.muv, muv)
        assert allclose(angles.B, B)
        assert allclose(angles.BDeg, BDeg)

        assert allclose(angles.shape[1], izaDegArray.shape[0])

        for i in range(angles.shape[1]):
            for j in range(angles.shape[0]):
                item = angles.array[j, i]

                assert item == angles.geometries[i][j]

        for i in range(angles.shape[1]):
            for j in range(angles.shape[0]):
                item = angles.arrayDeg[j, i]

                assert item == angles.geometriesDeg[i][j]


@pytest.mark.webtest
@pytest.mark.parametrize(
    "izaDegArray, vzaDegArray, raaDegArray, iaaDegArray, vaaDegArray, alphaDegArray, betaDegArray", [
        (np.arange(10, 11, 1), np.arange(10, 20, 1), np.arange(20, 21, 1), np.arange(30, 40, 1), np.arange(40, 50, 1),
         np.arange(50, 51, 1), np.arange(60, 70, 1)),
        (np.arange(10, 20, 1), np.arange(20, 30, 1), np.arange(30, 31, 1), np.arange(40, 50, 1), np.arange(50, 51, 1),
         np.arange(60, 61, 1), np.arange(70, 80, 1)),
        (np.arange(20, 30, 1), np.arange(30, 40, 1), np.arange(40, 50, 1), np.arange(50, 60, 1), np.arange(60, 70, 1),
         np.arange(70, 80, 1), np.arange(80, 81, 1)),
        (np.arange(30, 31, 1), np.arange(40, 41, 1), np.arange(50, 60, 1), np.arange(60, 61, 1), np.arange(70, 80, 1),
         np.arange(80, 90, 1), np.arange(90, 100, 1)),
        (np.arange(40, 50, 1), np.arange(50, 51, 1), np.arange(60, 70, 1), np.arange(70, 80, 1), np.arange(80, 90, 1),
         np.arange(90, 100, 1), np.arange(100, 110, 1)),
        (np.arange(50, 60, 1), np.arange(60, 61, 1), np.arange(70, 71, 1), np.arange(80, 90, 1), np.arange(90, 100, 1),
         np.arange(100, 110, 1), np.arange(110, 120, 1)),
        (np.arange(60, 70, 1), np.arange(70, 80, 1), np.arange(80, 90, 1), np.arange(90, 91, 1), np.arange(100, 110, 1),
         np.arange(110, 120, 1), np.arange(120, 121, 1)),

    ])
class TestAlignDeg:
    def test_deg2rad_raa(self, izaDegArray, vzaDegArray, raaDegArray, iaaDegArray, vaaDegArray, alphaDegArray,
                         betaDegArray):
        izaRadArray, vzaRadArray, raaRadArray, alphaRadArray, betaRadArray = (np.deg2rad(izaDegArray),
                                                                              np.deg2rad(vzaDegArray),
                                                                              np.deg2rad(raaDegArray),
                                                                              np.deg2rad(alphaDegArray),
                                                                              np.deg2rad(betaDegArray))

        mui, muv = np.cos(izaRadArray), np.cos(vzaRadArray)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegArray) + 1 / np.cos(vzaDegArray)

        angles = Angles(iza=izaDegArray, vza=vzaDegArray, raa=raaDegArray, alpha=alphaDegArray, beta=betaDegArray)

        assert np.all(angles.iza == izaRadArray) == True
        assert np.all(angles.vza == vzaRadArray) == True
        assert np.all(angles.raa == raaRadArray) == True
        assert np.all(angles.iaa == 0) == True
        assert np.all(angles.vaa == 0) == True
        assert np.all(angles.alpha == alphaRadArray) == True
        assert np.all(angles.beta == betaRadArray) == True

        assert np.all(angles.izaDeg == izaDegArray) == True
        assert np.all(angles.vzaDeg == vzaDegArray) == True
        assert np.all(angles.raaDeg == raaDegArray) == True
        assert np.all(angles.iaaDeg == 0) == True
        assert np.all(angles.vaaDeg == 0) == True
        assert np.all(angles.alphaDeg == alphaDegArray) == True
        assert np.all(angles.betaDeg == betaDegArray) == True

        assert np.all(angles.mui == mui) == True
        assert np.all(angles.muv == muv) == True
        assert np.all(angles.B == B) == True
        assert np.all(angles.BDeg == BDeg) == True

        for i in range(angles.shape[1]):
            for j in range(angles.shape[0]):
                item = angles.array[j, i]

                assert item == angles.geometries[i][j]

        for i in range(angles.shape[1]):
            for j in range(angles.shape[0]):
                item = angles.arrayDeg[j, i]

                assert item == angles.geometriesDeg[i][j]


class TestDtypeConversion:
    def test_deg2rad_raa(self):
        angles = Angles(iza=10, vza=10, raa=10, alpha=10, beta=10)

        for item in DTYPES:
            angles.dtype = item
            assert angles.dtype == item
            assert angles.array.dtype == item
            assert angles.arrayDeg.dtype == item


class TestAlignWith:
    def test_align_with_align_angle(self):
        angles = Angles(iza=10, vza=10, raa=10, alpha=10, beta=10)

        assert angles.shape == (7, 1)

        value = np.linspace(0, 10, 100)

        value = angles.align_with(value)

        assert angles.shape == (7, value.shape[1])

    def test_align_with_value(self):
        angles = Angles(iza=np.arange(0, 10, 1), vza=10, raa=10, alpha=10, beta=10)

        assert angles.shape == (7, 10)

        value = 2

        value = angles.align_with(value)

        assert angles.shape == (7, 10)
        assert value.shape[1] == angles.shape[1]


class TestNormalizeAndNbar:
    def test_normalize(self):
        angles = Angles(iza=10, vza=10, raa=10, alpha=10, beta=10, normalize=True)
        assert angles.shape == (7, 2)

        angles.normalize = False
        assert angles.normalize == False

        angles.normalize = 0
        assert angles.normalize == False
        assert angles.shape == (7, 1)

        angles.normalize = False
        assert angles.shape == (7, 1)

        angles.normalize = True
        assert angles.normalize == True

        angles.normalize = 1
        assert angles.normalize == True
        assert angles.shape == (7, 2)

        angles.normalize = True
        assert angles.shape == (7, 2)

    def test_normalize_array(self):
        iza, vza, raa, iaa, vaa, alpha, beta = (
            np.arange(10, 20, 1), np.arange(10, 20, 1), np.arange(20, 30, 1), np.arange(30, 40, 1),
            np.arange(40, 50, 1), np.arange(50, 51, 1), np.arange(60, 70, 1)
        )

        angles = Angles(iza=iza, vza=vza, raa=raa, alpha=alpha, beta=beta, normalize=True)
        assert angles.shape == (7, iza.shape[0] + 1)

        angles.normalize = False
        assert angles.shape == (7, iza.shape[0])

        angles.normalize = False
        assert angles.shape == (7, iza.shape[0])

        angles.normalize = True
        assert angles.shape == (7, iza.shape[0] + 1)

        angles.normalize = True
        assert angles.shape == (7, iza.shape[0] + 1)

    def test_nbar_DEG(self):
        angles = Angles(iza=10, vza=10, raa=10, alpha=10, beta=10, normalize=True)

        assert angles.nbar == angles.array[0][-1]

        angles.nbarDeg = 10

        assert angles.nbar == angles.array[0][-1]
        assert angles.nbarDeg == angles.arrayDeg[0][-1]

    def test_nbar_RAD(self):
        angles = Angles(iza=1, vza=1, raa=1, alpha=1, beta=10, normalize=True, angle_unit='RAD')

        assert angles.nbar == angles.array[0][-1]

        angles.nbarDeg = 10

        assert angles.nbar == angles.array[0][-1]
        assert angles.nbarDeg == angles.arrayDeg[0][-1]

        angles.nbar = 1

        assert angles.nbar == angles.array[0][-1]
        assert angles.nbarDeg == angles.arrayDeg[0][-1]
