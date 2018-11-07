import pytest
from numpy import radians, allclose, array

from radarpy import Angles


@pytest.mark.webtest
@pytest.mark.parametrize("izaDeg, vzaDeg, raaDeg, izaRad, vzaRad, raaRad", [
    (0, 0, 0, radians(0), radians(0), radians(0)),
    (35, 45, 50, radians(35), radians(45), radians(50))
])
class TestAnglesAngle:
    def test_normalize_iza_RAD(self, izaDeg, vzaDeg, raaDeg, izaRad, vzaRad, raaRad):
        kernel = Angles(izaDeg, vzaDeg, raaDeg, normalize=True)
        assert len(kernel.iza) == 2

    def test_normalize_iza_DEG(self, izaDeg, vzaDeg, raaDeg, izaRad, vzaRad, raaRad):
        kernel = Angles(izaDeg, vzaDeg, raaDeg, normalize=True, angle_unit='DEG')
        assert len(kernel.iza) == 2

    def test_kernel_DEG_iza(self, izaDeg, vzaDeg, raaDeg, izaRad, vzaRad, raaRad):
        kernel = Angles(izaDeg, vzaDeg, raaDeg)
        assert allclose(izaRad, kernel.iza[0], atol=1e-4)

    def test_kernel_DEG_vza(self, izaDeg, vzaDeg, raaDeg, izaRad, vzaRad, raaRad):
        kernel = Angles(izaDeg, vzaDeg, raaDeg)
        assert allclose(vzaRad, kernel.vza[0], atol=1e-4)

    def test_kernel_DEG_raa(self, izaDeg, vzaDeg, raaDeg, izaRad, vzaRad, raaRad):
        kernel = Angles(izaDeg, vzaDeg, raaDeg)
        assert allclose(raaRad, kernel.raa[0], atol=1e-4)

    def test_kernel_RAD_iza(self, izaRad, vzaRad, raaRad, izaDeg, vzaDeg, raaDeg):
        kernel = Angles(izaRad, vzaRad, raaRad, angle_unit='RAD')
        assert allclose(izaDeg, kernel.izaDeg[0], atol=1e-4)

    def test_kernel_RAD_vza(self, izaRad, vzaRad, raaRad, izaDeg, vzaDeg, raaDeg):
        kernel = Angles(izaRad, vzaRad, raaRad, angle_unit='RAD')
        assert allclose(vzaDeg, kernel.vzaDeg[0], atol=1e-4)

    def test_kernel_RAD_raa(self, izaRad, vzaRad, raaRad, izaDeg, vzaDeg, raaDeg):
        kernel = Angles(izaRad, vzaRad, raaRad, angle_unit='RAD')
        assert allclose(raaDeg, kernel.raaDeg[0], atol=1e-4)

    def test_align(self, izaRad, vzaRad, raaRad, izaDeg, vzaDeg, raaDeg):
        kernel = Angles(array([izaRad, 2, 3]), array([izaRad, 2]), array([izaRad]), angle_unit='RAD')
        assert len(array([izaRad, 2, 3])) == len(kernel.raaDeg)

    def test_align_except(self, izaRad, vzaRad, raaRad, izaDeg, vzaDeg, raaDeg):
        with pytest.raises(AssertionError):
            ang = Angles(array([izaRad, 2, 3]), array([izaRad, 2]), array([izaRad]), angle_unit='RAD', align=False)

    def test_unit_except(self, izaRad, vzaRad, raaRad, izaDeg, vzaDeg, raaDeg):
        with pytest.raises(ValueError):
            ang = Angles(array([izaRad, 2, 3]), array([izaRad, 2]), array([izaRad]), angle_unit='XXX', align=False)

    def test_dimension_except(self, izaRad, vzaRad, raaRad, izaDeg, vzaDeg, raaDeg):
        with pytest.raises(ValueError):
            ang = Angles(array([izaRad, 2, 3]), array([izaRad, 2]), array([izaRad]), angle_unit='XXX', align=False)
