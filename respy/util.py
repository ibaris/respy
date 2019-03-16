import numpy as np
from numpy import cos, tan, pi, asarray, pad, max, zeros, zeros_like
from respy.units.quantity import Quantity
from scipy import stats

__all__ = ["isquantity", "rad", "deg", "sec", "cot", "align_all", "max_length", "asarrays", "same_len",
           "stacks", "zeros_likes", "inf_to_num", "get_geometries", "chi", "same_shape", "isdim1",
           "Pearson", "RSME", "OpticalResult", "valid_dtype"]

DTYPES = [np.bool, np.byte, np.ubyte, np.short, np.ushort, np.intc, np.uintc, np.int_, np.uint, np.longlong,
          np.ulonglong, np.half, np.float, np.float16, np.single, np.double, np.longdouble, np.csingle, np.cdouble,
          np.clongdouble, np.int, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64,
          np.intp,
          np.uintp, np.float32, np.float64, np.complex, np.complex64, np.complex128, float, int, complex]

__ANGLE_UNIT_RAD__ = ['RAD', 'rad', 'radian', 'radians']
__ANGLE_UNIT_DEG__ = ['DEG', 'deg', 'degree', 'degrees']


def valid_dtype(dtype):
    if dtype in DTYPES:
        return True

    return False


def isquantity(*args):
    quantity = [hasattr(arg, "__QUANTITY__") for arg in args]

    return quantity[0] if len(quantity) == 1 else quantity


def rad(angle):
    """
    Convert degrees to radians.
    Parameter:
    ----------
    angle : (int, float or array_like)
        Angle in [DEG].
    """

    return angle * pi / 180.0


def deg(angle):
    """
    Convert radians to degree.
    Parameter:
    ----------
    angle : (int, float or array_like)
        Angle in [RAD].
    """

    return angle * 180. / pi


def sec(angle):
    """
    Secant of an angle.
    """
    return 1 / cos(angle)


def cot(x):
    """
    Cotangent of an angle.
    """
    return 1 / tan(x)


def align_all(data, constant_values='default', dtype=np.double):
    """
    Align the lengths of arrays.
    Parameters
    ----------
    data : tuple
        A tuple with (mixed) array_like, int, float.
    constant_values : int, float or 'default'
        The value at which the smaller values are expand. If 'default' (default) the last value will be choosed.
    dtype : type
        Data type of output.
    Returns
    -------
    aligned data : tuple
        Aligned tuple with array_like.
    """
    data = asarrays(data)
    max_len = max_length(data)

    if constant_values == 'default':
        return asarray(
            [pad(item, (0, max_len - len(item)), 'constant', constant_values=item[-1]) for item in data], dtype=dtype)
    else:
        return asarray(
            [pad(item, (0, max_len - len(item)), 'constant', constant_values=constant_values) for item in data],
            dtype=dtype)


def max_length(data):
    """
    Find the maximum length of the longest object in a tuple.
    Parameters
    ----------
    data : tuple
        A tuple with (mixed) array_like, int, float.
    Returns
    -------
    len : int
    """
    return max([len(item) for item in data])


def asarrays(data, dtype=None):
    """
    A wrapper of numpys asarrays for multiple data in a tuple.
    Parameters
    ----------
    data : tuple
        A tuple with (mixed) array_like, int, float.
    dtype : np.dtype
        Data type of output.
    Returns
    -------
    arrays : tuple
        A tuple with array_like.
    """
    if dtype is None:
        return [asarray(item).flatten() for item in data]
    else:
        return [asarray(item).flatten().astype(dtype) for item in data]


def same_len(data):
    """
    Determine if the items in a tuple has the same length.
    Parameters
    ----------
    data : tuple
        A tuple with (mixed) array_like, int, float.
    Returns
    -------
    bool
    """
    try:
        return all(len(item) == len(data[0]) for item in data)
    except TypeError:
        return False


def same_shape(data):
    """
    Determine if the arrays in a tuple has the same shape.
    Parameters
    ----------
    data : tuple
        A tuple with (mixed) array_like, int, float.
    Returns
    -------
    bool
    """
    try:
        return all(item.shape == data[0].shape for item in data)
    except TypeError:
        return False


def isdim1(data):
    """
    Determine if the arrays in a tuple has a dimension of 1.
    Parameters
    ----------
    data : tuple
        A tuple with (mixed) array_like, int, float.
    Returns
    -------
    bool
    """
    try:
        return all(item.ndim == 1 for item in data)

    except TypeError:
        return False


def stacks(items):
    try:
        shape = items[0].shape[0]

    except AttributeError:
        shape = 1

    array = zeros((len(items), shape))

    for i, item in enumerate(items):
        array[i] = item

    return array


def zeros_likes(data, rep=1, dtype=None):
    dtype = data.dtype if dtype is None else dtype

    return [zeros_like(data, dtype=dtype) for i in range(rep)]


def inf_to_num(data, num=0, nan=True):
    if type(data) == tuple or type(data) == list:
        data_list = list()
        for item in data:
            item[np.isinf(item)] = num
            if nan:
                item = np.nan_to_num(item)

            data_list.append(item)
        return data_list

    else:
        data[np.isneginf(data)] = num
        if nan:
            data = np.nan_to_num(data)

        return data


def get_geometries(type='HB', angle_unit="DEG"):
    """
    Function to return typical geometries for different aquicistions.
    Parameters
    ----------
    type : {'HB', 'HF', 'VB', 'VF'}
        Backscatter type:
            * HB: Horizontal Back Scattering (90.0, 90.0, 0.0, 180.0, 0.0, 0.0). Default.
            * HF: Horizontal Forward Scattering (90.0, 90.0, 0.0, 0.0, 0.0, 0.0).
            * VB: Vertical Back Scattering (0.0, 180.0, 0.0, 0.0, 0.0, 0.0).
            * VF: Vertical Forward Scattering (180.0, 180.0, 0.0, 0.0, 0.0, 0.0).
    angle_unit : {'RAD', 'DEG'}
        Output angle unit.
    Returns
    -------
    geometry : tuple
        A tuple with (iza, vza, iaa, vaa, alpha, beta) parameters.
    """
    if type is 'HB':
        return 90.0, 90.0, 0.0, 180.0, 0.0, 0.0
    elif type is 'HF':
        return 90.0, 90.0, 0.0, 0.0, 0.0, 0.0
    elif type is 'VB':
        return 0.0, 180.0, 0.0, 0.0, 0.0, 0.0
    elif type is 'VF':
        return 180.0, 180.0, 0.0, 0.0, 0.0, 0.0
    else:
        raise ValueError(
            "The parameter type should be 'HB', 'HF', 'VB', 'VF'. The actual parameter is: {0}".format(str(type)))


def chi(diameter, wavelength, unit=None):
    """
    Calculate the diameter of the particles scaled with respect to the wavelength: pi * diameter / wavelength.
    Parameters
    ----------
    diameter
    wavelength
    unit
    Returns
    -------
    """
    if isquantity(diameter):
        pass
    elif unit is None:
        raise AssertionError("If the parameter `diameter` is not a Quantity object, the unit must be defined.")
    else:
        diameter = Quantity(diameter, unit=unit)

    if isquantity(wavelength):
        pass
    elif unit is None:
        raise AssertionError("If the parameter `diameter` is not a Quantity object, the unit must be defined.")
    else:
        wavelength = Quantity(wavelength, unit=unit)

    if diameter.unit != wavelength.unit:
        diameter = diameter.convert_to(wavelength.unit)

    x = np.pi * diameter / wavelength
    x.set_name('Diameter scaled with respect to the wavelength.')
    x.set_constant(True)

    return np.pi * diameter / wavelength


def Pearson(x, y):
    return stats.pearsonr(x, y)[0]


def RSME(x, y):
    return np.sqrt(((x - y) ** 2).mean())


def UBRSME(x, y):
    return np.sqrt((((x - np.mean(x)) - (y - np.mean(y))) ** 2).mean())


class OpticalResult(dict):
    """ Represents the reflectance result.
    Returns
    -------
    All returns are attributes!
    BSC.U, BSC.VV, BSC.HH, BSC.VH, BSC.HV, BSC.array : array_like
        Radar backscattering values in [linear]. BSC.array contains the results as an array
        like array([BSC.U, BSC.VV, BSC.HH, BSC.VH, BSC.HV]).
    BSCdB.U, BSCdB.VV, BSCdB.HH, BSCdB.VH, BSCdB.HV, BSCdB.array : array_like
        Radar backscattering values in [linear]. BSC.array contains the results as an array
        like array([BSCdB.VV, BSCdB.HH, BSCdB.VH, BSCdB.HV]).
    I.U, I.VV, I.HH, I.VH, I.HV, I.array : array_like
        Intensity (BRDF) values. I.array contains the results as an array like array([I.U, I.VV, I.HH, I.VH, I.HV]).
    Bv.U, Bv.VV, Bv.HH, Bv.VH, Bv.HV, Bv.array : array_like
        Emissivity values (if available). Bv.array contains the results as an array
        like array([Bv.U, Bv.VV, Bv.HH, Bv.VH, Bv.HV]).
    Notes
    -----
    There may be additional attributes not listed above depending of the
    specific solver. Since this class is essentially a subclass of dict
    with attribute accessors, one can see which attributes are available
    using the `keys()` method.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

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
