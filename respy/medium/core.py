# -*- coding: utf-8 -*-
"""
Created on 26.02.2019 by Ismail Baris
"""
from __future__ import division
import warnings

__STOKES_TYPE__ = ['stokes', 'SV', 'Stokes']
__MOD_STOKES_TYPE__ = ['modified stokes', 'MSV', 'Modified Stokes', 'Modified', 'modified']
__EXT_STOKES_TYPE__ = ['extended stokes', 'EMSV', 'Extended Modified Stokes', 'extended']

class ComplexMedium(object):
    def __init__(self, Z, S=None, ks=None, ke=None, kt=None, N=1,  name=None, stokes_type='stokes', unit=None):
        """
        Build a complex media.

        Parameters
        ----------
        Z : callable
            A callable phase matrix whose output is a 4x4 array or a phase function whose output is a scalar array. The
            first two parameter must be the incidence zenith angle and the viewing zenith angle.
        S : callable, optional
            A callable scattering matrix whose output is a 2x2 array. The
            first two parameter must be the incidence zenith angle and the viewing zenith angle.
        ks : numpy.ndarray or object, optional
            Scattering coefficient. Only mandatory if S is None.
        ke : numpy.ndarray or object, optional
            Extinction coefficient. . Only mandatory if S is None.
        kt : numpy.ndarray or object, optional
            Extinction coefficient. . Only mandatory if S is None.
        N : int, array_like
            Number of scatterer in unit volume. Default is 1.

        name : str
            Name of the Medium.
        """

        if ks is None and ke is None and kt is None and S is None:
            raise AssertionError("To create a Complex Medium ks, ke and kt OR the Scattering Matrix S must be defined.")

        elif S is None and ks is None or ke is None or kt is None:
            if ks is None:
                raise AssertionError(
                    "If the Scattering Matrix S is None, ks, ke and kt must be defined. But ks is None.")
            if ke is None:
                raise AssertionError(
                    "If the Scattering Matrix S is None, ks, ke and kt must be defined. But ke is None.")
            if ke is None:
                raise AssertionError(
                    "If the Scattering Matrix S is None, ks, ke and kt must be defined. But kt is None.")

        elif not callable(Z):
            raise TypeError("The Phase Matrix or Function must be callable.")

        elif S is not None and not callable(S):
            raise TypeError("The Scattering Matrix must be callable.")

        self.name = name if name is not None else ''
        self.Z = Z
        self.S = S
        self.ks = ks
        self.ke = ke
        self.kt = kt

        self.stokes_type = stokes_type

    # --------------------------------------------------------------------------------------------------------
    # Magic Methods
    # --------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.name)

    def __Mij(self, iza, vza, *args):
        pass

    def compute_ke(self, iza, vza, *args):
        if self.ke is not None:
            warnings.warn("The extinction coefficient is alreads defined. Retuning None")
            return

        elif self.stokes_type in __STOKES_TYPE__:
            S = self.S(iza, vza, *args)




