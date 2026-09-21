from setuptools import setup, find_packages
from setuptools.extension import Extension
import numpy as np
import sys

C_COMPILE = True
USE_CYTHON = True

__version__ = "0.0.0"
exec(open('velocyto/_version.py').read())
print(sys.argv)

if C_COMPILE:
    package_data: dict = {}
    if USE_CYTHON:
        from Cython.Build import cythonize
        extensions = [Extension("velocyto.speedboosted",
                                ["velocyto/speedboosted.pyx"],
                                extra_compile_args=['-fopenmp', "-ffast-math"],  # NOTE optional flags -O3 -ffast-math -march=native
                                extra_link_args=['-fopenmp'])]
        extensions = cythonize(extensions, include_path=[np.get_include()])
    else:
        extensions = [Extension("velocyto.speedboosted",
                                ["velocyto/speedboosted.c"],
                                extra_compile_args=['-fopenmp', "-ffast-math"],
                                extra_link_args=['-fopenmp'])]
else:
    extensions = []
    if "darwin" in sys.platform:
        compiled = "velocyto/speedboosted.cpython-36m-darwin.so"
    elif "win" in sys.platform:
        sys.stdout.write("Sorry, we do not support (or like) Windows OS")
        sys.exit()
    elif "linux" in sys.platform:
        compiled = "velocyto/speedboosted.cpython-36m-x86_64-linux-gnu.so"
    package_data = {'velocyto': [compiled]}

setup(
    name="velocyto",
    version=__version__,
    packages=find_packages(),
    install_requires=['numpy>=1.19.5,<2.5',
                      'scipy>=1.5.3,!=1.16.*,<1.18',
                      'cython>=0.29.32,<4',
                      'numba>=0.50.1,<0.68',
                      'matplotlib>=3.5.3,<3.11',
                      'scikit-learn>=0.23.2,<1.8',
                      'h5py>=2.10.0,<4',
                      'loompy>=3.0.6,<4',
                      'pysam>=0.21.0,<0.24',
                      'Click>=8.1.3,<9',
                      'pandas>=1.3.5,<2.4'],
    # command
    entry_points='''
        [console_scripts]
        velocyto=velocyto.commands.velocyto:cli
    ''',
    ext_modules=extensions,
    include_dirs=[np.get_include()],
    package_data=package_data,
    # metadata
    author="Linnarsson Lab",
    author_email="sten.linnarsson@ki.se",
    url="https://github.com/velocyto-team/velocyto.py",
    download_url=f"https://github.com/velocyto-team/velocyto.py/archive/{__version__}.tar.gz",
    keywords=["RNAseq", "singlecell", "bioinformatics", "transcriptomics"],
    description="RNA velocity analysis for single cell RNA-seq data",
    license="BSD2")
