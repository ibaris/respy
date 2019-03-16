# -*- coding: utf-8 -*-
import sys
import warnings

import numpy as np

import respy.constants as const
from respy.util import (sec, align_all, asarrays, valid_dtype)
from respy.angles.auxil import check_angles, unit_is_deg, unit_is_rad

# from respy.units import Quantity, util

# python 3.6 comparability
if sys.version_info < (3, 0):
    srange = xrange
else:
    srange = range


class Angles(object):

    def __init__(self, iza, vza, raa=None, iaa=None, vaa=None, alpha=0.0, beta=0.0, normalize=False, nbar=0.0,
                 angle_unit='DEG', align=True, dtype=np.double):
        """ Angle Management System

        Angle is a class that helps you unify the different angles of the scanning geometry.

        Parameters
        ----------
        iza, vza, raa, iaa, vaa : int, float or array_like
            Incidence (iza) and scattering (vza) zenith angle, relative azimuth (raa) angle, incidence and viewing
            azimuth angle (ira, vra). If raa is defined, ira and vra are not mandatory.
        alpha, beta: int, float or array_like
            The Euler angles of the particle orientation (degrees).
        normalize : boolean, optional
            Set to 'True' to make kernels 0 at nadir view illumination. Since all implemented kernels are normalized
            the default value is False.
        nbar : float, optional
            The sun or incidence zenith angle at which the isotropic term is set
            to if normalize is True. The default value is 0.0.
        angle_unit : {'DEG', 'RAD', 'deg', 'rad'}, optional
            * 'DEG': All input angles (iza, vza, raa) are in [DEG] (default).
            * 'RAD': All input angles (iza, vza, raa) are in [RAD].
        align : boolean, optional
             Expand all input values to the same length (default).
        dtype : numpy.dtype
            Desired data type of all values. Default is np.double.

        Attributes
        ----------
        iza, vza, raa, iaa, vaa, alpha, beta: array_like
            SIncidence (iza) and scattering (vza) zenith angle, relative azimuth (raa) angle, incidence and viewing
            azimuth angle (ira, vra) in [RAD].
        izaDeg, vzaDeg, raaDeg, iaaDeg, vaaDeg, alphaDeg, betaDeg: array_like
            SIncidence (iza) and scattering (vza) zenith angle, relative azimuth (raa) angle, incidence and viewing
            azimuth angle (ira, vra) in [DEG].
        phi : array_like
            Relative azimuth angle in a range between 0 and 2pi.
        B, BDeg : array_like
            The result of (1/cos(vza)+1/cos(iza)).
        mui, muv : array_like
            Cosine of iza and vza in [RAD].
        geometries : tuple
            If raa is defined it shows a tuple with (iza, vza, raa, alpha, beta) in [RAD]. If iaa and vaa is defined
            the tuple will be (iza, vza, iaa, vaa, alpha, beta) in [RAD]
        geometriesDeg : tuple
            If raa is defined it shows a tuple with (iza, vza, raa, alpha, beta) in [DEG]. If iaa and vaa is defined
            the tuple will be (iza, vza, iaa, vaa, alpha, beta) in [DEG]
        nbar : float
            The sun or incidence zenith angle at which the isotropic term is set
            to if normalize is True. You can change this attribute within the class.
        normlaize : bool
            Set to 'True' to make kernels 0 at nadir view illumination. Since all implemented kernels are normalized
            the default value is False.
        dtype : numpy.dtype
            Desired data type of all values. This attribute is changeable.

        Methods
        -------
        align_with : Expand all input values to the same length depend on an external array.

        Note
        ----
        Hot spot direction is vza == iza and raa = 0.0

        """

        # Prepare Input Data -------------------------------------------------------------------------------------------
        iza, vza, raa, iaa, vaa, alpha, beta, raa_flag = check_angles(iza, vza, raa, iaa, vaa, alpha, beta, angle_unit,
                                                                      dtype)

        if align:
            iza, vza, raa, iaa, vaa, alpha, beta = align_all((iza, vza, raa, iaa, vaa, alpha, beta))

        temporal_array = np.asarray([iza, vza, raa, iaa, vaa, alpha, beta])

        # Check if all data has the same length
        if len({len(item) for item in temporal_array}) != 1:
            raise AssertionError("Input dimensions must agree. The actual dimensions are "
                                 "iza: {0}, vza: {1}, raa: {2}, iaa: {3}, vaa: {4}, "
                                 "alpha: {5} and beta: {6}".format(str(len(iza)), str(len(vza)), str(len(raa)),
                                                                   str(len(iaa)), str(len(vaa)), str(len(alpha)),
                                                                   str(len(beta))))

        # Convert Angles depending on Angle Unit -----------------------------------------------------------------------
        self.__normalize = normalize

        if unit_is_deg(angle_unit):
            self.__array = np.deg2rad(temporal_array)
            self.__nbar = np.deg2rad(nbar)

            self.__arrayDeg = temporal_array
            self.__nbarDeg = nbar

        elif unit_is_rad(angle_unit):
            self.__array = temporal_array
            self.__nbar = nbar

            self.__arrayDeg = np.rad2deg(temporal_array)
            self.__nbarDeg = np.rad2deg(nbar)

        # Normalize Angles depending on Parameter normalize ------------------------------------------------------------
        self.__array = self.__normalize_angles(self.__array, self.__nbar)
        self.__arrayDeg = self.__normalize_angles(self.__arrayDeg, self.__nbarDeg)

        # Check if there are negative angle values
        iza_mask = np.where(self.__array[0] < 0)[0]
        self.__array[0][iza_mask] = np.abs(self.__array[0][iza_mask])

        vza_mask = np.where(self.__array[1] < 0)[0]
        self.__array[1][vza_mask] = np.abs(self.__array[1][vza_mask])

        for item in self.__array[2:-2]:
            item[iza_mask] += const.pi
            item[vza_mask] += const.pi

        for itemDeg in self.__arrayDeg[2:-2]:
            itemDeg[iza_mask] += const.pi
            itemDeg[vza_mask] += const.pi

        # Set Attributes -----------------------------------------------------------------------------------------------
        self.__norm = None
        self.__dtype = dtype

        self.angle_unit = angle_unit
        self.align = align

    # ------------------------------------------------------------------------------------------------------------------
    # Magic Methods
    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        vals = dict()
        if self.normalize is False:
            vals['iza'], vals['izaDeg'] = self.iza.mean(), self.izaDeg.mean()
            vals['vza'], vals['vzaDeg'] = self.vza.mean(), self.vzaDeg.mean()
            vals['raa'], vals['raaDeg'] = self.raa.mean(), self.raaDeg.mean()
            vals['iaa'], vals['iaaDeg'] = self.iaa.mean(), self.iaaDeg.mean()
            vals['vaa'], vals['vaaDeg'] = self.vaa.mean(), self.vaaDeg.mean()
            vals['alpha'], vals['alphaDeg'] = self.alpha.mean(), self.alphaDeg.mean()
            vals['beta'], vals['betaDeg'] = self.beta.mean(), self.betaDeg.mean()
            vals['B'], vals['BDeg'] = self.B.mean(), self.BDeg.mean()
            vals['nbar'] = self.nbar

        else:
            vals['iza'], vals['izaDeg'] = self.iza[0:-1].mean(), self.izaDeg[0:-1].mean()
            vals['vza'], vals['vzaDeg'] = self.vza[0:-1].mean(), self.vzaDeg[0:-1].mean()
            vals['raa'], vals['raaDeg'] = self.raa[0:-1].mean(), self.raaDeg[0:-1].mean()
            vals['iaa'], vals['iaaDeg'] = self.iaa[0:-1].mean(), self.iaaDeg[0:-1].mean()
            vals['vaa'], vals['vaaDeg'] = self.vaa[0:-1].mean(), self.vaaDeg[0:-1].mean()
            vals['alpha'], vals['alphaDeg'] = self.alpha[0:-1].mean(), self.alphaDeg[0:-1].mean()
            vals['beta'], vals['betaDeg'] = self.beta[0:-1].mean(), self.betaDeg[0:-1].mean()
            vals['B'], vals['BDeg'] = self.B[0:-1].mean(), self.BDeg[0:-1].mean()
            vals['nbar'] = self.nbar

        info = 'Class                                    : Angles\n' \
               'Mean incidence zenith angle [RAD, DEG]   : {iza}, {izaDeg}\n' \
               'Mean viewing zenith angle [RAD, DEG]     : {vza}, {vzaDeg}\n' \
               'Mean relative azimuth angle [RAD, DEG]   : {raa}, {raaDeg}\n' \
               'Mean incidence azimuth angle [RAD, DEG]  : {iaa}, {iaaDeg}\n' \
               'Mean viewing azimuth angle [RAD, DEG]    : {vaa}, {vaaDeg}\n' \
               'Mean alpha angle [RAD, DEG]              : {alpha}, {alphaDeg}\n' \
               'Mean beta angle [RAD, DEG]               : {beta}, {betaDeg}\n' \
               'Mean B [RAD, DEG]                        : {B}, {BDeg}'.format(**vals)

        return info

    # def __repr__(self):
    #     names = ['Incidence Zenith Angle', 'Viewing Angle', 'Relative Azimuth Angle', 'Incidence Azimuth Angle',
    #              'Viewing Azimuth Angle', 'Euler Angle Alpha', 'Euler Angle Beta']
    # 
    #     prefix = '<{0} '.format(self.__class__.__name__)
    #     sep = ', '
    #     # iza, vza, raa, iaa, vaa, alpha, beta
    #     angle_str = list()
    #     if self.angle_unit is 'RAD' or self.angle_unit is 'rad':
    #         for i in range(self.array.shape[0]):
    #             angle_str.append(np.array2string(self.array[i],
    #                                              separator=sep,
    #                                              prefix=prefix))
    #         unit = util.radians
    # 
    #     else:
    #         for i in range(self.array.shape[0]):
    #             angle_str.append(np.array2string(self.arrayDeg[i],
    #                                              separator=sep,
    #                                              prefix=prefix))
    # 
    #         unit = util.degrees
    # 
    #     return_list = ''
    #     for i, item in enumerate(angle_str):
    #         return_list += "{0}{1} {2} in [{3}]>\n".format(prefix, item, names[i], unit)
    # 
    #     return return_list

    def __len__(self):
        return self.__array.shape[1]

    # ------------------------------------------------------------------------------------------------------------------
    # Property Access
    # ------------------------------------------------------------------------------------------------------------------
    # Access to Array Specific Attributes ------------------------------------------------------------------------------
    @property
    def len(self):
        """
        Length of array

        Returns
        -------
        len : int
        """
        return self.__array.shape[1]

    @property
    def shape(self):
        """
        Shape of array

        Returns
        -------
        shape : tuple
        """
        return self.__array.shape

    # Access to Angles -------------------------------------------------------------------------------------------------
    @property
    def iza(self):
        """
        Access the zenith angle of incidence [RAD].

        Returns
        -------
        iza : array_like
        """

        # # return Quantity(self.__array[0], unit=util.radians, name='Incidence Zenith Angle', constant=True)
        return self.__array[0]

    @property
    def izaDeg(self):
        """
        Access the zenith angle of incidence [DEG].

        Returns
        -------
        iza : array_like
        """
        # return Quantity(self.__arrayDeg[0], unit=util.degrees, name='Incidence Zenith Angle', constant=True)
        return self.__arrayDeg[1]

    @property
    def vza(self):
        """
        Access the zenith angle in viewing direction [RAD].

        Returns
        -------
        vza : array_like
        """
        # return Quantity(self.__array[1], unit=util.radians, name='Viewing Angle', constant=True)
        return self.__array[1]

    @property
    def vzaDeg(self):
        """
        Access the zenith angle in viewing direction [DEG].

        Returns
        -------
        vzaDeg : array_like
        """
        # # return Quantity(self.__arrayDeg[1], unit=util.degrees, name='Viewing Angle', constant=True)
        return self.__arrayDeg[1]

    @property
    def raa(self):
        """
        Access the relative azimuth angle [RAD].

        Note
        ----
        If iaa and raa is defined the relative azimuth angle is calculated like iaa - vaa.

        Returns
        -------
        raa : array_like
        """
        # return Quantity(self.__array[2], unit=util.radians, name='Relative Azimuth Angle', constant=True)
        return self.__array[2]

    @property
    def raaDeg(self):
        """
        Access the relative azimuth angle [DEG].

        Note
        ----
        If iaa and raa is defined the relative azimuth angle is calculated like iaa - vaa.

        Returns
        -------
        raaDeg : array_like
        """
        # return Quantity(self.__arrayDeg[2], unit=util.degrees, name='Relative Azimuth Angle', constant=True)
        return self.__arrayDeg[2]

    @property
    def iaa(self):
        """
        Access the azimuth angle of incidence [RAD].

        Note
        ----
        If only raa is defined the iaa and vaa are set to zero.

        Returns
        -------
        iaa : array_like
        """
        # return Quantity(self.__array[3], unit=util.radians, name='Incidence Azimuth Angle', constant=True)
        return self.__array[3]

    @property
    def iaaDeg(self):
        """
        Access the azimuth angle of incidence [DEG].

        Note
        ----
        If only raa is defined the iaa and vaa are set to zero.

        Returns
        -------
        iaaDeg : array_like
        """
        # return Quantity(self.__arrayDeg[3], unit=util.degrees, name='Incidence Azimuth Angle', constant=True)
        return self.__arrayDeg[3]

    @property
    def vaa(self):
        """
        Access the azimuth angle in viewing direction [RAD].

        Note
        ----
        If only raa is defined the iaa and vaa are set to zero.

        Returns
        -------
        vaa : array_like
        """
        # return Quantity(self.__array[4], unit=util.radians, name='Viewing Azimuth Angle', constant=True)
        return self.__array[4]

    @property
    def vaaDeg(self):
        """
        Access the azimuth angle of incidence [DEG].

        Note
        ----
        If only raa is defined the iaa and vaa are set to zero.

        Returns
        -------
        vaaDeg : array_like
        """
        # return Quantity(self.__arrayDeg[4], unit=util.degrees, name='Viewing Azimuth Angle', constant=True)
        return self.__arrayDeg[4]

    @property
    def alpha(self):
        """
        Access the Euler angle alpha of the particle orientation [RAD].

        Returns
        -------
        alpha : array_like
        """
        # return Quantity(self.__array[5], unit=util.radians, name='Euler Angle Alpha', constant=True)
        return self.__array[5]

    @property
    def alphaDeg(self):
        """
        Access the Euler angle alpha of the particle orientation [DEG].

        Returns
        -------
        alphaDeg : array_like
        """
        # return Quantity(self.__arrayDeg[5], unit=util.degrees, name='Euler Angle Alpha', constant=True)
        return self.__arrayDeg[5]

    @property
    def beta(self):
        """
        Access the Euler angle beta of the particle orientation [RAD].

        Returns
        -------
        beta : array_like
        """
        # return Quantity(self.__array[6], unit=util.radians, name='Euler Angle Beta', constant=True)
        return self.__array[6]

    @property
    def betaDeg(self):
        """
        Access the Euler angle beta of the particle orientation [DEG].

        Returns
        -------
        betaDeg : array_like
        """
        # return Quantity(self.__arrayDeg[6], unit=util.degrees, name='Euler Angle Beta', constant=True)
        return self.__arrayDeg[6]

    @property
    def B(self):
        """
        Access to the sum of the secants of the incidence and scattering angle [RAD].
        The calculation is like: sec(iza) + sec(vza)

        Returns
        -------
        B : array_like
        """
        B = sec(self.iza) + sec(self.vza)
        # B.set_name("Secants of iza + vza")
        # B.set_constant(True)
        return B

    @property
    def BDeg(self):
        """
        Access to the sum of the secants of the incidence and scattering angle [DEG].
        The calculation is like: sec(izaDeg) + sec(vzaDeg)

        Returns
        -------
        BDeg : array_like
        """
        B = sec(self.izaDeg) + sec(self.vzaDeg)
        # B.set_name("Secants of iza + vza")
        # B.set_constant(True)

        return B

    @property
    def mui(self):
        """
        Access the cosine zenith angle of incidence [RAD].

        Returns
        -------
        mui : array_like
        """
        mui = np.cos(self.iza)
        # mui.set_name("Cosine of iza")
        # mui.set_constant(True)

        return mui

    @property
    def muv(self):
        """
        Access the cosine zenith angle in viewing direction [RAD].

        Returns
        -------
        mui : array_like
        """
        muv = np.cos(self.vza)
        # muv.set_name("Cosine of vza")
        # muv.set_constant(True)

        return muv

    @property
    def phi(self):
        """
        Relative azimuth angle normalized in a range of 2*pi

        Returns
        -------
        phi : array_like
        """
        phi = np.abs((self.raa % (2. * const.pi)))
        # phi.set_name("Normalized Relative Azimuth Angle")
        # phi.set_constant(True)

        return phi

    @property
    def geometries(self):
        """
        Access the geometries as tuple objects [RAD].

        Returns
        -------
        geometries : tuple
        """
        geometries = [tuple(self.__array[:, i]) for i in srange(self.shape[1])]

        return tuple(geometries)

    @property
    def geometriesDeg(self):
        """
        Access the geometries as tuple objects [DEG].

        Returns
        -------
        geometriesDeg : tuple
        """

        geometriesDeg = [tuple(self.__arrayDeg[:, i]) for i in srange(self.shape[1])]

        return tuple(geometriesDeg)

    @property
    def array(self):
        return self.__array

    @property
    def arrayDeg(self):
        return self.__arrayDeg

    # ------------------------------------------------------------------------------------------------------------------
    # Property with Setter
    # ------------------------------------------------------------------------------------------------------------------
    # Conversion Routines ----------------------------------------------------------------------------------------------
    @property
    def dtype(self):
        """
        Access the dtype.

        Returns
        -------
        dtype : numpy.dtype
        """
        return self.__dtype

    @dtype.setter
    def dtype(self, value):
        """
        Define a new data type.

        Parameters
        ----------
        value : numpy.dtype

        Returns
        -------
        None
        """
        if value in DTYPES:
            pass
        else:
            raise TypeError("dtype must be a numpy.dtype object. The actual dtype is {0}".format(str(value)))

        self.__dtype = value

        if self.__dtype == np.int:
            warnings.warn("The dtype is np.int. This could lead to errors in unit radians.")

        self.__array = self.__change_dtype(self.__array, self.__nbar, self.__dtype)
        self.__arrayDeg = self.__change_dtype(self.__arrayDeg, self.__nbarDeg, self.__dtype)

    @property
    def nbar(self):
        """
        Access to the normalization factor nbar [RAD].

        Returns
        -------
        nbar : float
        """
        # return Quantity(self.__nbar, unit=util.rad, name='Normalization Angle', constant=True)

    @nbar.setter
    def nbar(self, value):
        """
        Define a new parameter for nbar.
        After the definition is done, the angles are normalized again as soon as the parameter 'normalize' is True.

        Parameters
        ----------
        value : float
            New nbar value in [RAD].

        Returns
        -------
        None
        """
        self.__nbar = value
        self.__nbarDeg = np.rad2deg(self.__nbar)

        if self.normalize is True:
            self.__array[0][-1] = self.__nbar
            self.__arrayDeg[0][-1] = self.__nbarDeg

        else:
            pass

    @property
    def nbarDeg(self):
        """
        Access to the normalization factor nbar [DEG].

        Returns
        -------
        nbar : float
        """
        return self.__nbarDeg

    @nbarDeg.setter
    def nbarDeg(self, value):
        """
        Define a new parameter for nbar.
        After the definition is done, the angles are normalized again as soon as the parameter 'normalize' is True.

        Parameters
        ----------
        value : float
            New nbar value in [DEG].

        Returns
        -------
        None
        """
        self.__nbarDeg = value
        self.__nbar = np.deg2rad(self.__nbarDeg)

        if self.normalize is True:
            self.__array[0][-1] = self.__nbar
            self.__arrayDeg[0][-1] = self.__nbarDeg

        else:
            pass

    @property
    def normalize(self):
        """
        Access to normalization.

        Returns
        -------
        normalize : bool
        """
        return self.__normalize

    @normalize.setter
    def normalize(self, value):
        """
        Define a new parameter for normalize.
        If value is True, the angles are normalized again as soon as the parameter 'normalize' is False.
        Otherwise (value is False), the angles are de-normalized again as soon as the parameter 'normalize' is True.

        Parameters
        ----------
        value : bool

        Returns
        -------
        None
        """
        if value is True or value is False:
            pass
        elif value == 1 or value == 0:
            value = True if value == 1 else False
        else:
            raise TypeError("Only bool type can be assigned.")

        if value is True:
            if self.__normalize is True:
                pass

            else:
                self.__normalize = value
                self.__array = self.__normalize_angles(self.__array, self.__nbar)
                self.__arrayDeg = self.__normalize_angles(self.__arrayDeg, self.__nbar)
        else:
            if self.__normalize is False:
                pass
            else:
                self.__array = np.delete(self.__array, np.s_[-1:], axis=1)
                self.__arrayDeg = np.delete(self.__arrayDeg, np.s_[-1:], axis=1)
                self.__normalize = value

    # ------------------------------------------------------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------------------------------------------------------
    def align_with(self, value):
        """
        Align all angles with another array.

        Parameters
        ----------
        value : array_like

        Returns
        -------
        value : array_like
            Align value.

        Note
        ----
        If len(value) > Angles.shape[1] then the angles inside Angles class will be aligned and it has no effect on
        value. If len(value) < Angles.shape[1] the output of value will be have the same len as Angles and it has no
        effect on the angles within the Angles class.
        """
        # RAD Angles
        data = [item for item in self.__array]

        if isinstance(value, tuple) or isinstance(value, list):
            data = tuple(value) + tuple(data, )
        else:
            data = (value,) + tuple(data, )

        data = align_all(data)

        # DEG Angles
        dataDeg = [item for item in self.__array]

        if isinstance(value, tuple):
            dataDeg = value + tuple(dataDeg, )
        else:
            dataDeg = (value,) + tuple(dataDeg, )

        dataDeg = align_all(dataDeg)

        self.__array = np.asarray(data[-7:])
        self.__arrayDeg = np.asarray(dataDeg[-7:])

        return data[0:-7]

    # ------------------------------------------------------------------------------------------------------------------
    # Private Methods
    # ------------------------------------------------------------------------------------------------------------------
    # Private Methods for Normalization and Conversion -----------------------------------------------------------------
    def __normalize_angles(self, array, nbar):
        if self.normalize:
            self.__norm = np.array([[nbar], [0], [0], [0], [0], [0], [0]])
            return np.append(array, self.__norm, axis=1)

        else:
            return array

    def __change_dtype(self, array, nbar, dtype):
        array = array.astype(dtype)
        return self.__normalize_angles(array, nbar)
