from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name = "grid.pyx",
    ext_modules = cythonize('grid.pyx'),
    include_dirs = [numpy.get_include()]# accepts a glob pattern
)
