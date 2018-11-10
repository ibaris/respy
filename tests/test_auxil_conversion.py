import numpy as np
import pytest

from respy import (BRF, BSC, BRDF, dB, sec, cot, linear, rad, deg, align_all)


@pytest.mark.webtest
@pytest.mark.parametrize("iza, vza, raa, ref", [
    (35, 30, 50, 0.01)
])
class TestRF:
    def test_BRF(self, iza, vza, raa, ref):
        test = BRF(ref)
        np.allclose(test, np.pi * ref)

    def test_BSC(self, iza, vza, raa, ref):
        test = BSC(ref, vza)
        np.allclose(test, ref * np.cos(vza) * 4 * np.pi)

    def test_BSC_DEG(self, iza, vza, raa, ref):
        test = BSC(ref, vza, angle_unit='DEG')
        np.allclose(test, ref * np.cos(np.radians(vza)) * (4 * np.pi))

    def test_BSC_error(self, iza, vza, raa, ref):
        with pytest.raises(ValueError):
            test = BSC(ref, vza, angle_unit='xxx')

    def test_BRDF(self, iza, vza, raa, ref):
        test = BRDF(ref, vza)
        np.allclose(test, ref / (np.cos(vza) * (4 * np.pi)))

    def test_BRDF_DEG(self, iza, vza, raa, ref):
        test = BRDF(ref, vza, angle_unit='DEG')
        np.allclose(test, ref / (np.cos(np.radians(vza)) * (4 * np.pi)))

    # def test_BRDF_error(self, vza, raa, ref):
    #     with pytest.raises(ValueError):
    #         test = BRDF(ref, vza, angle_unit='xxx')

    def test_dB(self, iza, vza, raa, ref):
        test = dB(ref)
        np.allclose(test, 10 * np.log10(ref))

    def test_linear(self, iza, vza, raa, ref):
        test1 = dB(ref)
        test2 = linear(ref)
        np.allclose(test1, test2)


class TestAuxil:
    def test_sec(self):
        test = sec(35)
        assert test == 1 / np.cos(35)

    def test_cot(self):
        test = cot(35)
        assert test == 1 / np.tan(35)

    def test_rad(self):
        xza = 35
        a = np.radians(xza)
        b = rad(xza)
        assert np.allclose(a, b)

    def test_deg(self):
        xza = 35
        a = np.radians(xza)
        b = rad(xza)
        a = np.degrees(a)
        b = deg(b)
        assert np.allclose(a, b)

    def test_allign_all(self):
        a = np.array([1, 2, 3])
        b = np.array([1, 2])

        a, b = align_all((a, b), constant_values=1)

        assert b[-1] == 1
