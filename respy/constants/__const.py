from __future__ import division
from respy.units import Quantity

k_B = Quantity(1.38064852e-23, name="Boltzmann constant", unit="joule / kelvin", constant=True)
c = Quantity(299792458.0, name="Speed of light in vacuum", unit="meter / second", constant=True)
h = Quantity(6.62606957e-34, name="Planck constant", unit="joule * second", constant=True)
pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164