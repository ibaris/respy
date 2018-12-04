import numpy as np
from numpy import cos, tan, pi, asarray, pad, max, zeros, zeros_like

DTYPES = [np.bool, np.byte, np.ubyte, np.short, np.ushort, np.intc, np.uintc, np.int_, np.uint, np.longlong,
          np.ulonglong, np.half, np.float, np.float16, np.single, np.double, np.longdouble, np.csingle, np.cdouble,
          np.clongdouble, np.int, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64,
          np.intp,
          np.uintp, np.float32, np.float64, np.complex, np.complex64, np.complex128, float, int, complex]

PI = 3.1415926535897932384626433832795028841971693993751058209749445923078164
C = 299792458

RAD_TO_DEG = 180.0 / PI
DEG_TO_RAD = PI / 180.0

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
    dtype : np.dtype
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
    return all(len(item) == len(data[0]) for item in data)


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
