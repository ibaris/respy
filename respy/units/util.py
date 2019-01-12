from __future__ import division
import sympy.physics.units as sympy_units
import sympy
from sympy.physics.units.quantities import Quantity
from sympy.physics.units.dimensions import frequency
from sympy import S

__OPERAND__ = ['*', '/', '+', '-']

One = S.One


def def_unit(unit):
    if not isinstance(unit, tuple(sympy.core.all_classes)):

        if isinstance(unit, str):

            if unit == "-":
                return unit

            else:
                unit = unit.split()

                unit_list = list()
                operand_list = list()

                for item in unit:
                    if item in __OPERAND__:
                        operand_list.append(item)
                    else:
                        try:
                            unit_list.append(__SELECT_UNIT__[item])

                        except KeyError:
                            raise AttributeError("{} is not a valid unit.".format(str(item)))

                unit = unit_list[0]

                for i in range(1, len(unit_list)):
                    item = unit_list[i]
                    try:
                        if operand_list[i - 1] == '*':
                            unit *= item
                        elif operand_list[i - 1] == '/':
                            unit /= item
                        elif operand_list[i - 1] == '+':
                            unit += item
                        elif operand_list[i - 1] == '-':
                            unit -= item
                    except IndexError:
                        pass

                return unit

        else:
            raise AttributeError("{} is not a valid unit.".format(str(unit)))
    else:
        return unit


decibel = dB = Quantity("decibel", abbrev="dB")
dB.set_dimension(One)
dB.set_scale_factor(One)

millihertz = mhz = mHz = Quantity("millihertz", abbrev="mHz")
millihertz.set_dimension(frequency)
millihertz.set_scale_factor(1 / 1e3)

centihertz = chz = cHz = Quantity("centihertz", abbrev="cHz")
centihertz.set_dimension(frequency)
centihertz.set_scale_factor(1 / 1e2)

decihertz = dhz = dHz = Quantity("decihertz", abbrev="dHz")
decihertz.set_dimension(frequency)
decihertz.set_scale_factor(1 / 1e1)

hertz = hz = Hz = Quantity("hertz", abbrev="Hz")
hertz.set_dimension(frequency)
hertz.set_scale_factor(One)

decahertz = dahz = daHz = Quantity("decahertz", abbrev="daHz")
decahertz.set_dimension(frequency)
decahertz.set_scale_factor(10)

hectohertz = hhz = hHz = Quantity("hectohertz", abbrev="hHz")
hectohertz.set_dimension(frequency)
hectohertz.set_scale_factor(100)

kilohertz = khz = kHz = Quantity("kilohertz", abbrev="kHz")
kilohertz.set_dimension(frequency)
kilohertz.set_scale_factor(1000)

megahertz = MHz = Quantity("megahertz", abbrev="MHz")
megahertz.set_dimension(frequency)
megahertz.set_scale_factor(1e6)

gigahertz = ghz = GHz = Quantity("gigahertz", abbrev="GHz")
gigahertz.set_dimension(frequency)
gigahertz.set_scale_factor(1e9)

terahertz = thz = THz = Quantity("terahertz", abbrev="THz")
terahertz.set_dimension(frequency)
terahertz.set_scale_factor(1e12)

petahertz = phz = PHz = Quantity("petahertz", abbrev="PHz")
petahertz.set_dimension(frequency)
petahertz.set_scale_factor(1e15)

nm = nanometers = nanometer = sympy_units.nm
um = micrometers = micrometer = sympy_units.um
mm = millimeters = millimeter = sympy_units.mm
cm = centimeters = centimeter = sympy_units.cm
dm = decimeters = decimeter = sympy_units.dm
m = meters = meter = sympy_units.m
km = kilometers = kilometer = sympy_units.km

s = second = seconds = sympy_units.second
minute = minutes = sympy_units.minute
h = hour = hours = sympy_units.hour

K = kelvins = kelvin = sympy_units.K

J = joules = joule = sympy_units.J

__SELECT_UNIT__ = {"-": None,

                   "decibel": decibel,
                   "dB": dB,

                   "millihertz": millihertz,
                   "mhz": mhz,
                   "mHz": mHz,
                   "centihertz": centihertz,
                   "chz": chz,
                   "cHz": cHz,
                   "decihertz": decihertz,
                   "dhz": dhz,
                   "dHz": dHz,
                   "hertz": hertz,
                   "hz": hz,
                   "Hz": Hz,
                   "decahertz": decahertz,
                   "dahz": dahz,
                   "daHz": daHz,
                   "hectohertz": hectohertz,
                   "hhz": hhz,
                   "hHz": hHz,
                   "kilohertz": kilohertz,
                   "khz": khz,
                   "kHz": kHz,
                   "megahertz": megahertz,
                   "MHz": MHz,
                   "gigahertz": gigahertz,
                   "ghz": ghz,
                   "GHz": GHz,
                   "terahertz": terahertz,
                   "thz": thz,
                   "THz": THz,
                   "petahertz": petahertz,
                   "phz": phz,
                   "PHz": PHz,

                   "nm": nm,
                   "um": um,
                   "mm": mm,
                   "cm": cm,
                   "dm": dm,
                   "m": m,
                   "km": km,

                   "nanometers": nanometers,
                   "micrometers": micrometers,
                   "millimeters": millimeters,
                   "centimeter": centimeter,
                   "decimeters": decimeters,
                   "meters": meters,
                   "kilometers": kilometers,

                   "nanometer": nanometer,
                   "micrometer": micrometer,
                   "millimeter": millimeter,
                   "centimeters": centimeters,
                   "decimeter": decimeter,
                   "meter": meter,
                   "kilometer": kilometer,

                   "second": second,
                   "minute": minute,
                   "hour": hour,

                   "seconds": seconds,
                   "minutes": minutes,
                   "hours": hours,

                   "s": s,
                   "h": h,

                   "K": K,
                   "kelvin": kelvin,
                   "kelvins": kelvins,

                   "J": J,
                   "joule": joule,
                   "joules": joules}
