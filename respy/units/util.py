from __future__ import division
import sympy.physics.units as sympy_units
import sympy
from sympy.physics.units.quantities import Quantity as sQuantity
from sympy.physics.units.dimensions import frequency as dim_frequency
from sympy import S

__OPERAND__ = ['*', '/', '+', '-', '**']

One = S.One


class UnitError(Exception):
    pass

class DimensionError(Exception):
    pass


class Units(dict):
    """ Storage for all units.

    Returns
    -------
    Dict with .dot access.

    Notes
    -----
    There may be additional attributes not listed above depending of the
    specific solver. Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method. adar Backscatter values of multi scattering contribution of surface and volume
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("{} is not a valid unit. Use `keys()` method to see all available units".format(name))

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())


class Frequency(dict):
    """ Storage for frequency units.

    Returns
    -------
    Dict with .dot access.

    Notes
    -----
    There may be additional attributes not listed above depending of the
    specific solver. Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method. adar Backscatter values of multi scattering contribution of surface and volume
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("{} is not a valid unit. Use `keys()` method to see all available units".format(name))

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())


class Length(dict):
    """ Storage for length units.

    Returns
    -------
    Dict with .dot access.

    Notes
    -----
    There may be additional attributes not listed above depending of the
    specific solver. Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method. adar Backscatter values of multi scattering contribution of surface and volume
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("{} is not a valid unit. Use `keys()` method to see all available units".format(name))

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())


class Energy(dict):
    """ Storage for energy units.

    Returns
    -------
    Dict with .dot access.

    Notes
    -----
    There may be additional attributes not listed above depending of the
    specific solver. Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method. adar Backscatter values of multi scattering contribution of surface and volume
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("{} is not a valid unit. Use `keys()` method to see all available units".format(name))

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())


class Time(dict):
    """ Storage for time units.

    Returns
    -------
    Dict with .dot access.

    Notes
    -----
    There may be additional attributes not listed above depending of the
    specific solver. Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method. adar Backscatter values of multi scattering contribution of surface and volume
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("{} is not a valid unit. Use `keys()` method to see all available units".format(name))

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())


class Temperature(dict):
    """ Storage for temperature units.

    Returns
    -------
    Dict with .dot access.

    Notes
    -----
    There may be additional attributes not listed above depending of the
    specific solver. Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method. adar Backscatter values of multi scattering contribution of surface and volume
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("{} is not a valid unit. Use `keys()` method to see all available units".format(name))

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())


class Other(dict):
    """ Storage for other, dimensionless units.

    Returns
    -------
    Dict with .dot access.

    Notes
    -----
    There may be additional attributes not listed above depending of the
    specific solver. Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method. adar Backscatter values of multi scattering contribution of surface and volume
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("{} is not a valid unit. Use `keys()` method to see all available units".format(name))

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, list(self.keys()))) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in sorted(self.items())])
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list(self.keys())


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
                            item = int(item)
                            unit_list.append(item)

                        except ValueError:
                            try:
                                unit_list.append(__UNITS__[item])

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
                        elif operand_list[i - 1] == '**':
                            unit **= item
                    except IndexError:
                        pass

                return unit

        else:
            raise AttributeError("{} is not a valid unit.".format(str(unit)))
    else:
        return unit


deg = degree = degrees = sympy_units.degree
rad = radian = radians = sympy_units.radian

decibel = dB = sQuantity("decibel", abbrev="dB")
dB.set_dimension(One)
dB.set_scale_factor(One)

millihertz = mhz = mHz = sQuantity("millihertz", abbrev="mHz")
millihertz.set_dimension(dim_frequency)
millihertz.set_scale_factor(1 / 1e3)

centihertz = chz = cHz = sQuantity("centihertz", abbrev="cHz")
centihertz.set_dimension(dim_frequency)
centihertz.set_scale_factor(1 / 1e2)

decihertz = dhz = dHz = sQuantity("decihertz", abbrev="dHz")
decihertz.set_dimension(dim_frequency)
decihertz.set_scale_factor(1 / 1e1)

hertz = hz = Hz = sQuantity("hertz", abbrev="Hz")
hertz.set_dimension(dim_frequency)
hertz.set_scale_factor(One)

decahertz = dahz = daHz = sQuantity("decahertz", abbrev="daHz")
decahertz.set_dimension(dim_frequency)
decahertz.set_scale_factor(10)

hectohertz = hhz = hHz = sQuantity("hectohertz", abbrev="hHz")
hectohertz.set_dimension(dim_frequency)
hectohertz.set_scale_factor(100)

kilohertz = khz = kHz = sQuantity("kilohertz", abbrev="kHz")
kilohertz.set_dimension(dim_frequency)
kilohertz.set_scale_factor(1000)

megahertz = MHz = sQuantity("megahertz", abbrev="MHz")
megahertz.set_dimension(dim_frequency)
megahertz.set_scale_factor(1e6)

gigahertz = ghz = GHz = sQuantity("gigahertz", abbrev="GHz")
gigahertz.set_dimension(dim_frequency)
gigahertz.set_scale_factor(1e9)

terahertz = thz = THz = sQuantity("terahertz", abbrev="THz")
terahertz.set_dimension(dim_frequency)
terahertz.set_scale_factor(1e12)

petahertz = phz = PHz = sQuantity("petahertz", abbrev="PHz")
petahertz.set_dimension(dim_frequency)
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

frequency = Frequency(millihertz=millihertz,
                      mhz=mhz,
                      mHz=mHz,
                      centihertz=centihertz,
                      chz=chz,
                      cHz=cHz,
                      decihertz=decihertz,
                      dhz=dhz,
                      dHz=dHz,
                      hertz=hertz,
                      hz=hz,
                      Hz=Hz,
                      decahertz=decahertz,
                      dahz=dahz,
                      daHz=daHz,
                      hectohertz=hectohertz,
                      hhz=hhz,
                      hHz=hHz,
                      kilohertz=kilohertz,
                      khz=khz,
                      kHz=kHz,
                      megahertz=megahertz,
                      MHz=MHz,
                      gigahertz=gigahertz,
                      ghz=ghz,
                      GHz=GHz,
                      terahertz=terahertz,
                      thz=thz,
                      THz=THz,
                      petahertz=petahertz,
                      phz=phz,
                      PHz=PHz)

length = Length(nm=nm,
                um=um,
                mm=mm,
                cm=cm,
                dm=dm,
                m=m,
                km=km,
                nanometers=nanometers,
                micrometers=micrometers,
                millimeters=millimeters,
                centimeter=centimeter,
                decimeters=decimeters,
                meters=meters,
                kilometers=kilometers,
                nanometer=nanometer,
                micrometer=micrometer,
                millimeter=millimeter,
                centimeters=centimeters,
                decimeter=decimeter,
                meter=meter,
                kilometer=kilometer)

time = Time(second=second,
            minute=minute,
            hour=hour,
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            s=s,
            h=h)

energy = Energy(J=J,
                joule=joule,
                joules=joules)

temperature = Temperature(K=K,
                          kelvin=kelvin,
                          kelvins=kelvins)

other = Other(decibel=decibel,
              dB=dB,
              deg=deg,
              degree=degree,
              degrees=degrees,
              rad=rad,
              radian=radian,
              radians=radians)

Units = Units(frequency=frequency, length=length, time=time, energy=energy, temperature=temperature, other=other)

def which_dimension(unit):
    pass


__UNITS__ = {"-": None,

             "decibel": decibel,
             "dB": dB,
             "deg": deg,
             "degree": degree,
             "degrees": degrees,
             "rad": rad,
             "radian": radian,
             "radians": radians,

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
