# -*- coding: utf-8 -*-
import numpy as np

from .auxiliary import (rad, deg, sec, align_all, asarrays)
import warnings


class Angles(object):

    def __init__(self, iza, vza, raa=None, iaa=None, vaa=None, alpha=0.0, beta=0.0, normalize=False, nbar=0.0,
                 angle_unit='DEG', align=True):
        """
        A class to deal with different angles.

        Parameters
        ----------
        iza, vza, raa, iaa, vaa : int, float or ndarray
            Incidence (iza) and scattering (vza) zenith angle, relative azimuth (raa) angle, incidence and viewing
            azimuth angle (ira, vra). If raa is defined, ira and vra are not mandatory.
        alpha, beta: int, float or array
            The Euler angles of the particle orientation (degrees).
        normalize : boolean, optional
            Set to 'True' to make kernels 0 at nadir view illumination. Since all implemented kernels are normalized
            the default value is False.
        nbar : float, optional
            The sun or incidence zenith angle at which the isotropic term is set
            to if normalize is True. The default value is 0.0.
        angle_unit : {'DEG', 'RAD'}, optional
            * 'DEG': All input angles (iza, vza, raa) are in [DEG] (default).
            * 'RAD': All input angles (iza, vza, raa) are in [RAD].
        align : boolean, optional
             Expand all input values to the same length (default).

        Returns
        -------
        All returns are attributes!
        iza, vza, raa, iaa, vaa, alpha, beta: array_like
            SIncidence (iza) and scattering (vza) zenith angle, relative azimuth (raa) angle, incidence and viewing
            azimuth angle (ira, vra) in [RAD].
        izaDeg, vzaDeg, raaDeg, iaaDeg, vaaDeg, alphaDeg, betaDeg: array_like
            SIncidence (iza) and scattering (vza) zenith angle, relative azimuth (raa) angle, incidence and viewing
            azimuth angle (ira, vra) in [DEG].
        phi : array_like
            Relative azimuth angle in a range between 0 and 2pi.
        B : array_like
            The result of (1/cos(vza)+1/cos(iza)).
        mui, muv : array_like
            Cosine of iza and vza in [RAD].
        geometries : tuple
            If raa is defined it shows a tuple with (iza, vza, raa, alpha, beta) in [RAD]. If iaa and vaa is defined
            the tuple will be (iza, vza, iaa, vaa, alpha, beta) in [RAD]
        geometriesDeg : tuple
            If raa is defined it shows a tuple with (iza, vza, raa, alpha, beta) in [DEG]. If iaa and vaa is defined
            the tuple will be (iza, vza, iaa, vaa, alpha, beta) in [DEG]
        Note
        ----
        Hot spot direction is vza == iza and raa = 0.0

        """

        # # Initialize values
        # if raa is None and iaa is None and vaa is None:
        #     raise AssertionError("At least raa or iaa and vaa should be defined.")
        #
        # elif raa is None:
        #     if iaa is None or vaa is None:
        #         raise AssertionError("If raa is not defined iaa AND vaa should be defined.")

        if raa is None:
            if iaa is None or vaa is None:
                raise AssertionError("If raa is not defined iaa AND vaa should be defined.")

            raa_flag = False
            self.iaa = iaa
            self.vaa = vaa
            self.raa = iaa - vaa

        else:
            raa_flag = True
            self.raa = raa
            self.iaa = np.zeros_like(raa)
            self.vaa = np.zeros_like(raa)

        self.vza = vza
        self.iza = iza
        self.beta = beta
        self.alpha = alpha

        self.normalize = normalize
        self.nbar = nbar
        self.angle_unit = angle_unit

        # Assertions
        if self.angle_unit != 'DEG' and self.angle_unit != 'RAD':
            raise AssertionError(
                "angle_unit must be 'DEG' or 'RAD', but angle_unit is: {}".format(str(self.angle_unit)))

        # Initialize angle information
        self.__pre_process(align)
        self.__set_angle()
        self.__set_geometries(raa_flag)

    def normalization(self, kernel=None, args=None):
        if args is None and kernel is None:
            raise ValueError("kernel or/ and args must be defined.")
        else:
            if args is None:
                kernel = kernel - kernel[-1]
                return kernel

            elif kernel is None:
                return [item[0:-1] for item in args]

            else:
                kernel = kernel - kernel[-1]
                list_args = list(args)
                list_args.append(kernel)
                args = tuple(list_args)
                return [item[0:-1] for item in args]

    def __pre_process(self, align):
        self.iza, self.vza, self.raa, self.iaa, self.vaa, self.alpha, self.beta = asarrays(
            (self.iza, self.vza, self.raa, self.iaa, self.vaa, self.alpha, self.beta))

        if align:
            self.iza, self.vza, self.raa, self.iaa, self.vaa, self.alpha, self.beta = align_all(
                (self.iza, self.vza, self.raa, self.iaa, self.vaa, self.alpha, self.beta))

        else:
            # try:
            if len(self.vza) != len(self.iza) or len(self.vza) != len(self.raa):
                raise AssertionError("Input dimensions must agree. "
                                     "The actual dimensions are "
                                     "iza: {0}, vza: {1} and raa: {2}".format(str(len(self.iza)),
                                                                              str(len(self.vza)),
                                                                              str(len(self.raa))))

            # except (AttributeError, TypeError):
            #     pass

    def __set_angle(self):
        """
        A method to store and organize the input angle data. This also convert
        all angle data in degrees to radians.
        """

        if self.angle_unit is 'DEG':
            self.vzaDeg = self.vza.flatten()
            self.izaDeg = self.iza.flatten()
            self.raaDeg = self.raa.flatten()
            self.iaaDeg = self.iaa.flatten()
            self.vaaDeg = self.vaa.flatten()
            self.alphaDeg = self.alpha.flatten()
            self.betaDeg = self.beta.flatten()

            if self.normalize:
                # calculate nadir term by extending array
                self.vzaDeg = np.array(list(self.vzaDeg) + [0.0]).flatten()
                self.izaDeg = np.array(list(self.izaDeg) + [self.nbar]).flatten()
                self.raaDeg = np.array(list(self.raaDeg) + [0.0]).flatten()
                self.iaaDeg = np.array(list(self.iaaDeg) + [0.0]).flatten()
                self.vaaDeg = np.array(list(self.vaaDeg) + [0.0]).flatten()
                self.alphaDeg = np.array(list(self.alphaDeg) + [0.0]).flatten()
                self.betaDeg = np.array(list(self.betaDeg) + [0.0]).flatten()

                self.BDeg = (sec(np.mean(rad(self.izaDeg[0:-1]))) + sec(np.mean(rad(self.vzaDeg[0:-1]))))
            else:
                self.BDeg = (sec(np.mean(rad(self.izaDeg))) + sec(np.mean(rad(self.vzaDeg))))

            self.vza = rad(self.vzaDeg)
            self.iza = rad(self.izaDeg)
            self.raa = rad(self.raaDeg)
            self.iaa = rad(self.iaaDeg)
            self.vaa = rad(self.vaaDeg)
            self.alpha = rad(self.alphaDeg)
            self.beta = rad(self.betaDeg)

            # Check if there are negative angle values
            w = np.where(self.vza < 0)[0]
            self.vza[w] = -self.vza[w]
            self.raa[w] = self.raa[w] + np.pi
            w = np.where(self.iza < 0)[0]
            self.iza[w] = -self.iza[w]
            self.raa[w] = self.raa[w] + np.pi
            self.iaa[w] = self.iaa[w] + np.pi
            self.vaa[w] = self.vaa[w] + np.pi
            self.alpha[w] = self.alpha[w] + np.pi
            self.beta[w] = self.beta[w] + np.pi

            # Turn the raa values in to a range between 0 and 2*pi
            try:
                self.phi = np.abs((self.raa % (2. * np.pi)))
            except TypeError:
                warnings.warn('The parameter Phi could not be computed. It will be replaced by self.raa')

                self.phi = self.raa

        if self.angle_unit is 'RAD':
            self.vza = self.vza.flatten()
            self.iza = self.iza.flatten()
            self.raa = self.raa.flatten()
            self.iaa = self.iaa.flatten()
            self.vaa = self.vaa.flatten()
            self.alpha = self.alpha.flatten()
            self.beta = self.beta.flatten()

            if self.normalize:
                # calculate nadir term by extending array
                self.vza = np.array(list(self.vza) + [0.0]).flatten()
                self.iza = np.array(list(self.iza) + [self.nbar]).flatten()
                self.raa = np.array(list(self.raa) + [0.0]).flatten()
                self.iaa = np.array(list(self.iaa) + [0.0]).flatten()
                self.vaa = np.array(list(self.vaa) + [0.0]).flatten()
                self.B = (sec(np.mean(self.iza[0:-1])) + sec(np.mean(self.vza[0:-1])))

            else:
                self.B = (sec(np.mean(self.iza)) + sec(np.mean(self.vza)))

            # Check if there are negative angle values
            w = np.where(self.vza < 0)[0]
            self.vza[w] = -self.vza[w]
            self.raa[w] = self.raa[w] + np.pi
            w = np.where(self.iza < 0)[0]
            self.iza[w] = -self.iza[w]
            self.raa[w] = self.raa[w] + np.pi
            self.iaa[w] = self.iaa[w] + np.pi
            self.vaa[w] = self.vaa[w] + np.pi

            self.vzaDeg = deg(self.vza)
            self.izaDeg = deg(self.iza)
            self.raaDeg = deg(self.raa)
            self.iaaDeg = deg(self.iaa)
            self.vaaDeg = deg(self.vaa)
            self.alphaDeg = deg(self.alpha)
            self.betaDeg = deg(self.beta)

            # Turn the raa values in to a range between 0 and 2 pi
            try:
                self.phi = np.abs((self.raa % (2. * np.pi)))
            except TypeError:
                warnings.warn('The parameter Phi could not be computed. It will be replaced by self.raa')

                self.phi = self.raa

        self.mui = np.cos(self.iza)
        self.muv = np.cos(self.vza)

    def __set_geometries(self, raa_flag):

        if raa_flag:
            self.geometries = tuple(
                [(self.iza[i], self.vza[i], self.raa[i], self.alpha[i], self.beta[i]) for i
                 in range(len(self.iza))])

            self.geometriesDeg = tuple(
                [(self.izaDeg[i], self.vzaDeg[i], self.raaDeg[i], self.alphaDeg[i], self.betaDeg[i]) for
                 i
                 in range(len(self.izaDeg))])

        else:
            self.geometries = tuple(
                [(self.iza[i], self.vza[i], self.iaa[i], self.vaa[i], self.alpha[i], self.beta[i]) for i
                 in range(len(self.iza))])

            self.geometriesDeg = tuple(
                [(self.izaDeg[i], self.vzaDeg[i], self.iaaDeg[i], self.vaaDeg[i], self.alphaDeg[i], self.betaDeg[i]) for
                 i
                 in range(len(self.izaDeg))])
