from numpy import cos, tan, pi, asarray, pad, max


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


def align_all(data, constant_values='default'):
    max_len = max_length(data)

    if constant_values == 'default':
        return asarray(
            [pad(item, (0, max_len - len(item)), 'constant', constant_values=item[-1]) for item in data])
    else:
        return asarray(
            [pad(item, (0, max_len - len(item)), 'constant', constant_values=constant_values) for item in data])


def max_length(data):
    return max([len(item) for item in data])


def asarrays(data):
    return [asarray(item).flatten() for item in data]


def same_len(args):
    return all(len(item) == len(args[0]) for item in args)
