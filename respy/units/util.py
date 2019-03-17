# -*- coding: utf-8 -*-
"""
Utility for Physical Quantities
-------------------------------
Created on 20.01.2019 by Ismail Baris

This module defines all units of `Quantity` objects.
"""

from __future__ import division

import sys

from respy.bin_units.wrapper import (dim_isnone, get_unitstr, unit_isnone, get_unit, get_dim, dim_isone, dim_iszero)
from respy.units.unit import __unit__, __values__
from respy.units.dimensions import *

python3 = False if sys.version_info < (3, 0) else True


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


class Power(dict):
    """ Storage for power units.

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


class Mass(dict):
    """ Storage for mass units.

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


class Current(dict):
    """ Storage for current units.

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


class Volume(dict):
    """ Storage for Volume units.

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


class Area(dict):
    """ Storage for Volume units.

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


class Angle(dict):
    """ Storage for other, angle units.

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
    # Units = Units()
    Frequency = Frequency()
    Length = Length()
    Energy = Energy()
    Power = Power()
    Time = Time()
    Temperature = Temperature()
    Mass = Mass()
    Current = Current()
    Other = Other()
    Area = Area()
    Angle = Angle()
    Volume = Volume()

    __unit_dict__ = {"frequency": Frequency,
                     'length': Length,
                     "energy": Energy,
                     "power": Power,
                     "time": Time,
                     "temperature": Temperature,
                     'mass': Mass,
                     "current": Current,
                     'other': Other,
                     'area': Area,
                     'volume': Volume,
                     'angle': Angle}

    dimensions = {'angle': angle, 'area': area, 'volume': volume, 'frequency': frequency, 'length': length,
                  'energy': energy, 'power': power,
                  'temperature': temperature, 'time': time, 'mass': mass,
                  'current': current}

    def __init__(self):
        self.__unit_dict = Units.__unit_dict__
        self.units = dict(zip(__unit__, __values__))
        self.dimensions = Units.dimensions

        self.__setup_units()

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

    def __setup_units(self):
        """
        Setup Unit class with all available units and dimensions.

        Returns
        -------
        None
        """
        for item in self.units.keys():
            dimension = self.units[item].dimension.name

            if dim_isnone(self.units[item]) or dim_isone(self.units[item]) or dim_iszero(self.units[item]):
                self.__unit_dict['other'][str(item)] = self.units[item]
            else:
                self.__unit_dict[str(dimension)][str(item)] = self.units[item]

        for item in self.__unit_dict.keys():
            self[item] = self.__unit_dict[item]

    @staticmethod
    def str2unit(unit):
        """
        Get a unit object from a str or char*.

        Parameters
        ----------
        unit : str or char*
            Desired unit in str format.

        Returns
        -------
        object

        Notes
        -----
        str2unit works only with strings. Function `get_unit` can handle also sympy expressions and None-Type units and
        dimension.
        """
        return get_unitstr(unit)

    @staticmethod
    def unit2str(unit):
        """
        Get a str from a unit object.

        Parameters
        ----------
        unit : object
            Desired unit in str format.

        Returns
        -------
        str

        """
        if unit_isnone(unit):
            return b''
        else:
            return str(unit)

    @staticmethod
    def get_unit(unit):
        """
        Get unit object from string or unit object (sympy).

        Parameters
        ----------
        unit : str, char or unit object.

        Returns
        -------
        object

        Notes
        -----
        str2unit works only with strings. This function can handle also sympy expressions and None-Type units and
        dimension.
        """
        return get_unit(unit)

    @staticmethod
    def get_dim(unit):
        """
        Get dimension from a unit object.

        Parameters
        ----------
        unit : object
            Unit expression.

        Returns
        -------
        dimension
        """
        return get_dim(unit)

    @staticmethod
    def unit_isnone(unit):
        """
        Check if a unit has a None-Typed object.

        Parameters
        ----------
        unit : object
            Unit expression.

        Returns
        -------
        bool
        """
        return unit_isnone(unit)

    @staticmethod
    def dim_isnone(unit):
        """
        Check if a dimension of a unit has a None-Typed object.

        Parameters
        ----------
        unit : object
            Unit expression.

        Returns
        -------
        bool
        """
        return dim_isnone(unit)

    @staticmethod
    def dim_iszero(unit):
        """
        Check if a dimension of a unit is Zero.

        Parameters
        ----------
        unit : object
            Unit expression.

        Returns
        -------
        bool
        """
        return dim_iszero(unit)


Units = Units()
