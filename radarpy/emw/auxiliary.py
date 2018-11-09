CONVERT_FREQ = {'Hz': 1,
                'daHz': 1e1,
                'hHz': 1e2,
                'kHz': 1e3,
                'MHz': 1e6,
                'GHz': 1e9,
                'THz': 1e12,
                'PHz': 1e15}

CONVERT_WAVE = {'nm': 1e9,
                'um': 1e6,
                'mm': 1e3,
                'cm': 1e2,
                'dm': 1e1,
                'm': 1,
                'km': 1e-3}

BANDS = ["VIS", "NIR", "SWIR", "MWIR", "LWIR", "L", "S", "C", "X", "Ku", "K", "Ka", "V", "W", "D"]


def check_unit_frequency(unit):
    if unit in CONVERT_FREQ.keys():
        return None
    else:
        raise ValueError("Unit of frequency must be {0}.".format(str(CONVERT_FREQ.keys())))


def check_unit_wavelength(unit):
    if unit in CONVERT_WAVE.keys():
        return None
    else:
        raise ValueError("Unit of wavelength must be {0}.".format(str(CONVERT_WAVE.keys())))
