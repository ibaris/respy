# -*- coding: UTF-8 -*-

"""
(c) 2017- Ismail Baris
For COPYING and LICENSE details, please refer to the LICENSE file
"""

try:
    from pip import main as pipmain

except ImportError:
    from pip._internal import main as pipmain

import pip
from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install


def get_version():
    version = dict()

    with open("radarpy/version.py") as fp:
        exec (fp.read(), version)

    return version['__version__']


def get_packages():
    find_packages(exclude=['docs', 'tests', 'invert']),
    return find_packages()


setup(name='radarpy',

      version=get_version(),
      description='Fundamental Formulas for Radar and Angle Management',
      packages=get_packages(),
      # package_dir={'dir': 'dir', 'dir': 'dir',
      #              'dir': 'dir', 'dir': 'dir'},

      author="Ismail Baris",
      maintainer='Ismail Baris',

      # ~ license='APACHE 2',

      url='https://github.com/ibaris/radarpy',

      long_description='Fundamental Formulas for Radar and Angle Management',
      # install_requires=install_requires,

      keywords=["radar", "remote-sensing", "optics", "integration",
                "microwave", "estimation", "physics", "radiative transfer"],

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "License :: Other/Proprietary License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",

      ],
      include_package_data=True,
      install_requires=['numpy'],
      setup_requires=[
          'pytest-runner',
      ],
      tests_require=[
          'pytest',
      ],
      )
