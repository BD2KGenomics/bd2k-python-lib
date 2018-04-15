import sys

assert sys.version_info >= (2, 6)

from setuptools import setup, find_packages

kwargs = dict(
    name="bd2k-python-lib",
    version="1.14a1",

    author='Hannes Schmidt',
    author_email='hannes@ucsc.edu',
    url='https://github.com/BD2KGenomics/bd2k-python-lib',
    description='The BD2K Python module kitchen sink',

    package_dir={ '': 'src' },
    packages=find_packages( 'src' ),
    install_requires=[ 'future' ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest==3.5.0',
        'mock==1.0.1',
        'lockfile==0.11.0',
        'boto==2.38.0'],
    namespace_packages=[ 'bd2k' ] )

setup( **kwargs )
