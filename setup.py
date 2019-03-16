# -*- coding: UTF-8 -*-
# distutils: include_dirs = respy/unit_base

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

    with open("respy/___version___.py") as fp:
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
    print ('******** Start compiling with CYTHON ********')

    ext_modules += [
        Extension("respy.bin_units.conversion", ["respy/bin_units/conversion.pyx"], include_dirs=['.']),
        Extension("respy.bin_units.auxil", ["respy/bin_units/auxil.pyx"], include_dirs=['.']),
        Extension("respy.bin_units.decomposition", ["respy/bin_units/decomposition.pyx"], include_dirs=['.']),
        Extension("respy.bin_units.util", ["respy/bin_units/util.pyx"], include_dirs=['.']),
        Extension("respy.bin_units.wrapper", ["respy/bin_units/wrapper.pyx"], include_dirs=['.']),


        Extension("respy.unit_base.auxil", ["respy/unit_base/auxil.pyx"], include_dirs=['.']),
        Extension("respy.unit_base.convert", ["respy/unit_base/convert.pyx"], include_dirs=['.']),
        Extension("respy.unit_base.operations", ["respy/unit_base/operations.pyx"], include_dirs=['.']),
        Extension("respy.unit_base.util", ["respy/unit_base/util.pyx"], include_dirs=['.'])
    ]

    cmdclass.update({'build_ext': build_ext})

    print ('******** Compiling with CYTHON accomplished ********')

else:
    print ('******** CYTHON Not Found. Use distributed .c files ********')

    ext_modules += [
        Extension("respy.unit_base.auxil", ["respy/unit_base/auxil.c"], include_dirs=['.']),
        Extension("respy.unit_base.convert", ["respy/unit_base/convert.c"], include_dirs=['.']),
        Extension("respy.unit_base.operations", ["respy/unit_base/operations.c"], include_dirs=['.']),
        Extension("respy.unit_base.util", ["respy/unit_base/util.c"], include_dirs=['.'])
    ]
    print ('******** Compiling with distributed Files accomplished ********')

setup(name='respy',

      version=get_version(),
      description='Fundamental Formulas for Radar and Angle Management',
      packages=get_packages(),

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
      package_data={
          'respy/unit_base': ['*.pxd', '*.c'],
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=['numpy'],
      setup_requires=[
          'pytest-runner',
      ],
      tests_require=[
          'pytest',
      ],
      )
