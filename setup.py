# -*- coding: UTF-8 -*-

"""
(c) 2017- Ismail Baris
For COPYING and LICENSE details, please refer to the LICENSE file
"""
try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False

else:
    use_cython = True

try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

from setuptools import find_packages
import numpy

def get_version():
    version = dict()

    with open("respy/version.py") as fp:
        exec (fp.read(), version)

    return version['__version__']


def get_packages():
    find_packages(exclude=['docs', 'tests', 'invert']),
    return find_packages()


# with open('requirements.txt') as f:
#     required = f.read().splitlines()

cmdclass = {}
ext_modules = []

if use_cython:
    print ('******** Compiling with CYTHON accomplished ******')

    ext_modules += [
        Extension("respy.base.unit_base",
                  ["respy/base/unit_base.pyx"], include_dirs=['.'])
    ]

    cmdclass.update({'build_ext': build_ext})

else:
    print ('******** CYTHON Not Found. Use distributed .c files *******')

    ext_modules += [
        Extension("respy.base.unit_base",
                  ["respy/base/unit_base.c"], include_dirs=['.'])
    ]

setup(name='respy',

      version=get_version(),
      description='Fundamental Formulas for Radar and Angle Management',
      packages=get_packages(),
      # package_dir={'dir': 'dir', 'dir': 'dir',
      #              'dir': 'dir', 'dir': 'dir'},

      cmdclass=cmdclass,

      include_dirs=[numpy.get_include()],
      ext_modules=ext_modules,

      author="Ismail Baris",
      maintainer='Ismail Baris',

      # ~ license='APACHE 2',

      url='https://github.com/ibaris/respy',

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
