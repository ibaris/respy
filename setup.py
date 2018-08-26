# -*- coding: UTF-8 -*-

"""
(c) 2017- Ismail Baris
For COPYING and LICENSE details, please refer to the LICENSE file
"""

import pip
from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install


class install_local(install):
    def run(self):
        install.run(self)
        pip.main(['install',
                  'dependence'])


def get_packages():
    find_packages(exclude=['docs', 'tests', 'invert']),
    return find_packages()


setup(name='radarpy',

      version='0.0.1',

      description='Fundamental Formulas for Radar',
      cmdclass={'install': install_local},
      packages=get_packages(),
      # package_dir={'dir': 'dir', 'dir': 'dir',
      #              'dir': 'dir', 'dir': 'dir'},

      author="Ismail Baris",
      maintainer='Ismail Baris',

      # ~ license='APACHE 2',

      url='https://github.com/ibaris/radarpy',

      long_description='Fundamental Formulas for Radar',
      # install_requires=install_requires,

      keywords=["radar", "remote-sensing", "optics", "integration",
                "microwave", "estimation", "physics", "radiative transfer"],

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Atmospheric Science',

          # Pick your license as you wish (should match "license" above)
          # ~ 'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 2.7',
          'Operating System :: Microsoft',

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
