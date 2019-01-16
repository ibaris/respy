from respy.units.quantity import Quantity
import numpy as np

__REGION__ = ['OPTIC', 'OPTICS', 'RADAR', 'TIR', 'THERMAL', 'RADIO', 'UHF', 'SHF', 'EHF', 'THF']

__BANDS__ = {"GAMMA": "GAMMA",
             "XRAY": "XRAY",
             "UV": "UV",
             "VIS": "OPTIC",
             "NIR": "OPTIC",
             "SWIR": "OPTIC",
             "MWIR": "THERMAL",
             "LWIR": "THERMAL",
             "L": "MICROWAVE",
             "S": "MICROWAVE",
             "C": "MICROWAVE",
             "X": "MICROWAVE",
             "Ku": "MICROWAVE",
             "K": "MICROWAVE",
             "Ka": "MICROWAVE",
             "V": "MICROWAVE",
             "W": "MICROWAVE",
             "D": "MICROWAVE",
             "ELF": "RADIO",
             "SLF": "RADIO",
             "ULF": "RADIO",
             "VLF": "RADIO",
             "LF": "RADIO",
             "MF": "RADIO",
             "HF": "RADIO",
             "VHF": "RADIO"}

__WHICH__BAND__ = {"GAMMA": Quantity(np.linspace(0, 1, 2), 'nm'),
                   "XRAY": Quantity(np.linspace(1.1, 10, 2), 'nm'),
                   "UV": Quantity(np.linspace(10.1, 400, 2), 'nm'),
                   "VIS": Quantity(np.linspace(400, 750, 2), 'nm'),
                   "NIR": Quantity(np.linspace(751, 1000, 2), 'nm'),
                   "SWIR": Quantity(np.linspace(1001., 2500, 2), 'nm'),

                   "MWIR": Quantity(np.linspace(3000., 5000, 2), 'nm'),
                   "LWIR": Quantity(np.linspace(8000., 12000, 2), 'nm'),

                   "L": Quantity(np.linspace(1, 2.0, 2), 'GHz'),
                   "S": Quantity(np.linspace(2.1, 4, 2), 'GHz'),
                   "C": Quantity(np.linspace(4.1, 8, 2), 'GHz'),
                   "X": Quantity(np.linspace(8.1, 12, 2), 'GHz'),
                   "Ku": Quantity(np.linspace(12.1, 18, 2), 'GHz'),
                   "K": Quantity(np.linspace(18.1, 26.5, 2), 'GHz'),
                   "Ka": Quantity(np.linspace(26.6, 40, 2), 'GHz'),
                   "V": Quantity(np.linspace(50.1, 75, 2), 'GHz'),
                   "W": Quantity(np.linspace(75.1, 110, 2), 'GHz'),
                   "D": Quantity(np.linspace(110.1, 170, 2), 'GHz'),

                   "ELF": Quantity(np.linspace(3, 30, 2), 'Hz'),
                   "SLF": Quantity(np.linspace(30.1, 300, 2), 'Hz'),
                   "ULF": Quantity(np.linspace(300.1, 3000, 2), 'Hz'),
                   "VLF": Quantity(np.linspace(3.1, 30, 2), 'kHz'),
                   "LF": Quantity(np.linspace(30.1, 300, 2), 'kHz'),
                   "MF": Quantity(np.linspace(0.31, 3, 2), 'MHz'),
                   "HF": Quantity(np.linspace(3.1, 30, 2), 'MHz'),
                   "VHF": Quantity(np.linspace(30.1, 300, 2), 'MHz')}

__WHICH__REGION__ = {"GAMMA": Quantity(np.linspace(0, 1, 2), 'nm'),
                     "XRAY": Quantity(np.linspace(1.1, 10, 2), 'nm'),
                     "UV": Quantity(np.linspace(10.1, 400, 2), 'nm'),
                     "OPTIC": Quantity(np.linspace(400, 2500, 2), 'nm'),

                     "TIR": Quantity(np.linspace(3000., 12000, 2), 'nm'),

                     "MICROWAVE": Quantity(np.linspace(1, 170, 2), 'GHz'),

                     "RADIO": Quantity(np.linspace(3, 300000000, 2), 'Hz'),

                     "UHF": Quantity(np.linspace(0.31, 0.9, 2), 'GHz'),
                     "EHF": Quantity(np.linspace(170.1, 300, 2), 'GHz'),
                     "THF": Quantity(np.linspace(0.31, 3, 2), 'THz')}