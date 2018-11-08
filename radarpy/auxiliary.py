from numpy import cos, tan, pi, asarray, pad, max, zeros, zeros_like
import numpy as np

CONVERT_FREQ = {'Hz': 1, 'MHz': 1e6, 'GHz': 1e9, 'THz': 1e12}
CONVERT_WAVE = {'m': 1, 'cm': 100, 'nm': 1e+9}

DTYPES = [np.bool, np.byte, np.ubyte, np.short, np.ushort, np.intc, np.uintc, np.int_, np.uint, np.longlong,
          np.ulonglong, np.half, np.float, np.float16, np.single, np.double, np.longdouble, np.csingle, np.cdouble,
          np.clongdouble, np.int, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64,
          np.intp,
          np.uintp, np.float32, np.float64, np.complex, np.complex64, np.complex128, float, int, complex]


def check_unit_frequency(unit):
    if unit == "Hz" or unit == "MHz" or unit == "GHz" or unit == "THz":
        return None
    else:
        raise ValueError("unit must be MHz, GHz or THz.")


def check_unit_wavelength(unit):
    if unit == "m" or unit == "cm" or unit == "nm":
        return None
    else:
        raise ValueError("unit must be m, cm or nm.")


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
    return max([len(item) for item in data])


def asarrays(data, dtype=None):
    if dtype is None:
        return [asarray(item).flatten() for item in data]
    else:
        return [asarray(item).flatten().astype(dtype) for item in data]


def same_len(args):
    return all(len(item) == len(args[0]) for item in args)


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


def get_geometries(type='HB'):
    """
    Function to return typical geometries for different aquicistions.

    Parameters
    ----------
    type : {'HB', 'HF', 'VB', 'VF'}
        Backscatter type:
            * HB: Horizontal Back Scattering (90.0, 90.0, 0.0, 180.0, 0.0, 0.0).
            * HF: Horizontal Forward Scattering (90.0, 90.0, 0.0, 0.0, 0.0, 0.0).
            * VB: Vertical Back Scattering (0.0, 180.0, 0.0, 0.0, 0.0, 0.0).
            * VF: Vertical Forward Scattering (180.0, 180.0, 0.0, 0.0, 0.0, 0.0).

    Returns
    -------
    geometry : tuple
        A tuple with (iza, vza, iaa, vaa, alpha, beta) parameters.

    """
    if type is 'HB':
        return (90.0, 90.0, 0.0, 180.0, 0.0, 0.0)
    elif type is 'HF':
        return (90.0, 90.0, 0.0, 0.0, 0.0, 0.0)
    elif type is 'VB':
        return (0.0, 180.0, 0.0, 0.0, 0.0, 0.0)
    elif type is 'VF':
        return (180.0, 180.0, 0.0, 0.0, 0.0, 0.0)
    else:
        raise ValueError(
            "The parameter type should be 'HB', 'HF', 'VB', 'VF'. The actual parameter is: {0}".format(str(type)))
