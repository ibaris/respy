from __future__ import division
import pytest
from numpy import radians, allclose, array
import numpy as np
from radarpy import Angles, DTYPES


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

        angle = Angles(iza=izaDegSingle, vza=vzaDegSingle, raa=raaDegSingle, alpha=alphaDegSingle, beta=betaDegSingle)

        assert allclose(angle.iza, izaRadSingle)
        assert allclose(angle.vza, vzaRadSingle)
        assert allclose(angle.raa, raaRadSingle)
        assert allclose(angle.iaa, 0)
        assert allclose(angle.vaa, 0)
        assert allclose(angle.alpha, alphaRadSingle)
        assert allclose(angle.beta, betaRadSingle)

        assert allclose(angle.izaDeg, izaDegSingle)
        assert allclose(angle.vzaDeg, vzaDegSingle)
        assert allclose(angle.raaDeg, raaDegSingle)
        assert allclose(angle.iaaDeg, 0)
        assert allclose(angle.vaaDeg, 0)
        assert allclose(angle.alphaDeg, alphaDegSingle)
        assert allclose(angle.betaDeg, betaDegSingle)

        assert allclose(angle.mui, mui)
        assert allclose(angle.muv, muv)
        assert allclose(angle.B, B)
        assert allclose(angle.BDeg, BDeg)

    def test_deg2rad_iaa_vaa(self, izaDegSingle, vzaDegSingle, raaDegSingle, iaaDegSingle, vaaDegSingle,
                             alphaDegSingle, betaDegSingle):
        izaRadSingle, vzaRadSingle, iaaRadSingle, vaaRadSingle, alphaRadSingle, betaRadSingle = (
            np.deg2rad(izaDegSingle), np.deg2rad(vzaDegSingle),
            np.deg2rad(iaaDegSingle), np.deg2rad(vaaDegSingle), np.deg2rad(alphaDegSingle), np.deg2rad(betaDegSingle))

        mui, muv = np.cos(izaRadSingle), np.cos(vzaRadSingle)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegSingle) + 1 / np.cos(vzaDegSingle)

        angle = Angles(iza=izaDegSingle, vza=vzaDegSingle, iaa=iaaDegSingle, vaa=vaaDegSingle, alpha=alphaDegSingle,
                       beta=betaDegSingle)

        assert allclose(angle.iza, izaRadSingle)
        assert allclose(angle.vza, vzaRadSingle)
        assert allclose(angle.iaa, iaaRadSingle)
        assert allclose(angle.vaa, vaaRadSingle)
        assert allclose(angle.raa, iaaRadSingle - vaaRadSingle)
        assert allclose(angle.alpha, alphaRadSingle)
        assert allclose(angle.beta, betaRadSingle)

        assert allclose(angle.izaDeg, izaDegSingle)
        assert allclose(angle.vzaDeg, vzaDegSingle)
        assert allclose(angle.iaaDeg, iaaDegSingle)
        assert allclose(angle.vaaDeg, vaaDegSingle)
        assert allclose(angle.raaDeg, iaaDegSingle - vaaDegSingle)
        assert allclose(angle.alphaDeg, alphaDegSingle)
        assert allclose(angle.betaDeg, betaDegSingle)

        assert allclose(angle.mui, mui)
        assert allclose(angle.muv, muv)
        assert allclose(angle.B, B)
        assert allclose(angle.BDeg, BDeg)


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

        angle = Angles(iza=izaRadSingle, vza=vzaRadSingle, raa=raaRadSingle, alpha=alphaRadSingle, beta=betaRadSingle,
                       angle_unit='RAD')

        assert allclose(angle.iza, izaRadSingle)
        assert allclose(angle.vza, vzaRadSingle)
        assert allclose(angle.raa, raaRadSingle)
        assert allclose(angle.iaa, 0)
        assert allclose(angle.vaa, 0)
        assert allclose(angle.alpha, alphaRadSingle)
        assert allclose(angle.beta, betaRadSingle)

        assert allclose(angle.izaDeg, izaDegSingle)
        assert allclose(angle.vzaDeg, vzaDegSingle)
        assert allclose(angle.raaDeg, raaDegSingle)
        assert allclose(angle.iaaDeg, 0)
        assert allclose(angle.vaaDeg, 0)
        assert allclose(angle.alphaDeg, alphaDegSingle)
        assert allclose(angle.betaDeg, betaDegSingle)

        assert allclose(angle.mui, mui)
        assert allclose(angle.muv, muv)
        assert allclose(angle.B, B)
        assert allclose(angle.BDeg, BDeg)

    def test_deg2rad_iaa_vaa(self, izaRadSingle, vzaRadSingle, raaRadSingle, iaaRadSingle, vaaRadSingle,
                             alphaRadSingle, betaRadSingle):
        izaDegSingle, vzaDegSingle, iaaDegSingle, vaaDegSingle, alphaDegSingle, betaDegSingle = (
            np.rad2deg(izaRadSingle), np.rad2deg(vzaRadSingle),
            np.rad2deg(iaaRadSingle), np.rad2deg(vaaRadSingle), np.rad2deg(alphaRadSingle), np.rad2deg(betaRadSingle))

        mui, muv = np.cos(izaRadSingle), np.cos(vzaRadSingle)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegSingle) + 1 / np.cos(vzaDegSingle)

        angle = Angles(iza=izaRadSingle, vza=vzaRadSingle, iaa=iaaRadSingle, vaa=vaaRadSingle, alpha=alphaRadSingle,
                       beta=betaRadSingle, angle_unit='RAD')

        assert allclose(angle.iza, izaRadSingle)
        assert allclose(angle.vza, vzaRadSingle)
        assert allclose(angle.iaa, iaaRadSingle)
        assert allclose(angle.vaa, vaaRadSingle)
        assert allclose(angle.raa, iaaRadSingle - vaaRadSingle)
        assert allclose(angle.alpha, alphaRadSingle)
        assert allclose(angle.beta, betaRadSingle)

        assert allclose(angle.izaDeg, izaDegSingle)
        assert allclose(angle.vzaDeg, vzaDegSingle)
        assert allclose(angle.iaaDeg, iaaDegSingle)
        assert allclose(angle.vaaDeg, vaaDegSingle)
        assert allclose(angle.raaDeg, iaaDegSingle - vaaDegSingle)
        assert allclose(angle.alphaDeg, alphaDegSingle)
        assert allclose(angle.betaDeg, betaDegSingle)

        assert allclose(angle.mui, mui)
        assert allclose(angle.muv, muv)
        assert allclose(angle.B, B)
        assert allclose(angle.BDeg, BDeg)


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

        angle = Angles(iza=izaDegArray, vza=vzaDegArray, raa=raaDegArray, alpha=alphaDegArray, beta=betaDegArray)

        assert allclose(angle.iza, izaRadArray)
        assert allclose(angle.vza, vzaRadArray)
        assert allclose(angle.raa, raaRadArray)
        assert allclose(angle.iaa, 0)
        assert allclose(angle.vaa, 0)
        assert allclose(angle.alpha, alphaRadArray)
        assert allclose(angle.beta, betaRadArray)

        assert allclose(angle.izaDeg, izaDegArray)
        assert allclose(angle.vzaDeg, vzaDegArray)
        assert allclose(angle.raaDeg, raaDegArray)
        assert allclose(angle.iaaDeg, 0)
        assert allclose(angle.vaaDeg, 0)
        assert allclose(angle.alphaDeg, alphaDegArray)
        assert allclose(angle.betaDeg, betaDegArray)

        assert allclose(angle.mui, mui)
        assert allclose(angle.muv, muv)
        assert allclose(angle.B, B)
        assert allclose(angle.BDeg, BDeg)

        assert allclose(angle.shape[1], izaDegArray.shape[0])

    def test_deg2rad_iaa_vaa(self, izaDegArray, vzaDegArray, raaDegArray, iaaDegArray, vaaDegArray,
                             alphaDegArray, betaDegArray):
        izaRadArray, vzaRadArray, iaaRadArray, vaaRadArray, alphaRadArray, betaRadArray = (
            np.deg2rad(izaDegArray), np.deg2rad(vzaDegArray),
            np.deg2rad(iaaDegArray), np.deg2rad(vaaDegArray), np.deg2rad(alphaDegArray), np.deg2rad(betaDegArray))

        mui, muv = np.cos(izaRadArray), np.cos(vzaRadArray)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegArray) + 1 / np.cos(vzaDegArray)

        angle = Angles(iza=izaDegArray, vza=vzaDegArray, iaa=iaaDegArray, vaa=vaaDegArray, alpha=alphaDegArray,
                       beta=betaDegArray)

        assert allclose(angle.iza, izaRadArray)
        assert allclose(angle.vza, vzaRadArray)
        assert allclose(angle.iaa, iaaRadArray)
        assert allclose(angle.vaa, vaaRadArray)
        assert allclose(angle.raa, iaaRadArray - vaaRadArray)
        assert allclose(angle.alpha, alphaRadArray)
        assert allclose(angle.beta, betaRadArray)

        assert allclose(angle.izaDeg, izaDegArray)
        assert allclose(angle.vzaDeg, vzaDegArray)
        assert allclose(angle.iaaDeg, iaaDegArray)
        assert allclose(angle.vaaDeg, vaaDegArray)
        assert allclose(angle.raaDeg, iaaDegArray - vaaDegArray)
        assert allclose(angle.alphaDeg, alphaDegArray)
        assert allclose(angle.betaDeg, betaDegArray)

        assert allclose(angle.mui, mui)
        assert allclose(angle.muv, muv)
        assert allclose(angle.B, B)
        assert allclose(angle.BDeg, BDeg)

        assert allclose(angle.shape[1], izaDegArray.shape[0])


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

        angle = Angles(iza=izaRadArray / 100., vza=vzaRadArray / 100., raa=raaRadArray / 100.,
                       alpha=alphaRadArray / 100.,
                       beta=betaRadArray / 100.,
                       angle_unit='RAD')

        assert allclose(angle.iza, izaRadArray / 100)
        assert allclose(angle.vza, vzaRadArray / 100)
        assert allclose(angle.raa, raaRadArray / 100)
        assert allclose(angle.iaa, 0)
        assert allclose(angle.vaa, 0)
        assert allclose(angle.alpha, alphaRadArray / 100)
        assert allclose(angle.beta, betaRadArray / 100)

        assert allclose(angle.izaDeg, izaDegArray)
        assert allclose(angle.vzaDeg, vzaDegArray)
        assert allclose(angle.raaDeg, raaDegArray)
        assert allclose(angle.iaaDeg, 0)
        assert allclose(angle.vaaDeg, 0)
        assert allclose(angle.alphaDeg, alphaDegArray)
        assert allclose(angle.betaDeg, betaDegArray)

        assert allclose(angle.mui, mui)
        assert allclose(angle.muv, muv)
        assert allclose(angle.B, B)
        assert allclose(angle.BDeg, BDeg)

        assert allclose(angle.shape[1], izaDegArray.shape[0])

    def test_Rad2rad_iaa_vaa(self, izaRadArray, vzaRadArray, raaRadArray, iaaRadArray, vaaRadArray,
                             alphaRadArray, betaRadArray):
        izaDegArray, vzaDegArray, iaaDegArray, vaaDegArray, alphaDegArray, betaDegArray = (
            np.rad2deg(izaRadArray / 100.), np.rad2deg(vzaRadArray / 100.),
            np.rad2deg(iaaRadArray / 100.), np.rad2deg(vaaRadArray / 100.), np.rad2deg(alphaRadArray / 100.),
            np.rad2deg(betaRadArray / 100.))

        mui, muv = np.cos(izaRadArray / 100), np.cos(vzaRadArray / 100)
        B = 1 / mui + 1 / muv
        BDeg = 1 / np.cos(izaDegArray) + 1 / np.cos(vzaDegArray)

        angle = Angles(iza=izaRadArray / 100., vza=vzaRadArray / 100., iaa=iaaRadArray / 100., vaa=vaaRadArray / 100.,
                       alpha=alphaRadArray / 100.,
                       beta=betaRadArray / 100., angle_unit='RAD')

        assert allclose(angle.iza, izaRadArray / 100)
        assert allclose(angle.vza, vzaRadArray / 100)
        assert allclose(angle.iaa, iaaRadArray / 100)
        assert allclose(angle.vaa, vaaRadArray / 100)
        assert allclose(angle.raa, iaaRadArray / 100 - vaaRadArray / 100)
        assert allclose(angle.alpha, alphaRadArray / 100)
        assert allclose(angle.beta, betaRadArray / 100)

        assert allclose(angle.izaDeg, izaDegArray)
        assert allclose(angle.vzaDeg, vzaDegArray)
        assert allclose(angle.iaaDeg, iaaDegArray)
        assert allclose(angle.vaaDeg, vaaDegArray)
        assert allclose(angle.raaDeg, iaaDegArray - vaaDegArray)
        assert allclose(angle.alphaDeg, alphaDegArray)
        assert allclose(angle.betaDeg, betaDegArray)

        assert allclose(angle.mui, mui)
        assert allclose(angle.muv, muv)
        assert allclose(angle.B, B)
        assert allclose(angle.BDeg, BDeg)

        assert allclose(angle.shape[1], izaDegArray.shape[0])


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

        angle = Angles(iza=izaDegArray, vza=vzaDegArray, raa=raaDegArray, alpha=alphaDegArray, beta=betaDegArray)

        assert np.all(angle.iza == izaRadArray) == True
        assert np.all(angle.vza == vzaRadArray) == True
        assert np.all(angle.raa == raaRadArray) == True
        assert np.all(angle.iaa == 0) == True
        assert np.all(angle.vaa == 0) == True
        assert np.all(angle.alpha == alphaRadArray) == True
        assert np.all(angle.beta == betaRadArray) == True

        assert np.all(angle.izaDeg == izaDegArray) == True
        assert np.all(angle.vzaDeg == vzaDegArray) == True
        assert np.all(angle.raaDeg == raaDegArray) == True
        assert np.all(angle.iaaDeg == 0) == True
        assert np.all(angle.vaaDeg == 0) == True
        assert np.all(angle.alphaDeg == alphaDegArray) == True
        assert np.all(angle.betaDeg == betaDegArray) == True

        assert np.all(angle.mui == mui) == True
        assert np.all(angle.muv == muv) == True
        assert np.all(angle.B == B) == True
        assert np.all(angle.BDeg == BDeg) == True


class TestDtypeConversion:
    def test_deg2rad_raa(self):
        angle = Angles(iza=10, vza=10, raa=10, alpha=10, beta=10)

        for item in DTYPES:
            angle.dtype = item
            assert angle.dtype == item
            assert angle.array.dtype == item
            assert angle.arrayDeg.dtype == item


class TestNormalizeAndNbar:
    def test_normalize(self):
        angle = Angles(iza=10, vza=10, raa=10, alpha=10, beta=10, normalize=True)
        assert angle.shape == (7, 2)

        angle.normalize = False
        assert angle.shape == (7, 1)

        angle.normalize = False
        assert angle.shape == (7, 1)

        angle.normalize = True
        assert angle.shape == (7, 2)

        angle.normalize = True
        assert angle.shape == (7, 2)

    def test_normalize_array(self):
        iza, vza, raa, iaa, vaa, alpha, beta = (
            np.arange(10, 20, 1), np.arange(10, 20, 1), np.arange(20, 30, 1), np.arange(30, 40, 1),
            np.arange(40, 50, 1), np.arange(50, 51, 1), np.arange(60, 70, 1)
        )

        angle = Angles(iza=iza, vza=vza, raa=raa, alpha=alpha, beta=beta, normalize=True)
        assert angle.shape == (7, iza.shape[0] + 1)

        angle.normalize = False
        assert angle.shape == (7, iza.shape[0])

        angle.normalize = False
        assert angle.shape == (7, iza.shape[0])

        angle.normalize = True
        assert angle.shape == (7, iza.shape[0] + 1)

        angle.normalize = True
        assert angle.shape == (7, iza.shape[0] + 1)

    def test_nbar_DEG(self):
        angle = Angles(iza=10, vza=10, raa=10, alpha=10, beta=10, normalize=True)

        assert angle.nbar == angle.array[0][-1]

        angle.nbarDeg = 10

        assert angle.nbar == angle.array[0][-1]
        assert angle.nbarDeg == angle.arrayDeg[0][-1]

    def test_nbar_RAD(self):
        angle = Angles(iza=1, vza=1, raa=1, alpha=1, beta=10, normalize=True, angle_unit='RAD')

        assert angle.nbar == angle.array[0][-1]

        angle.nbarDeg = 10

        assert angle.nbar == angle.array[0][-1]
        assert angle.nbarDeg == angle.arrayDeg[0][-1]

        angle.nbar = 1

        assert angle.nbar == angle.array[0][-1]
        assert angle.nbarDeg == angle.arrayDeg[0][-1]
