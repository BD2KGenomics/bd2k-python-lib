import sys

assert sys.version_info >= (2, 6)

from setuptools import setup, find_packages

kwargs = dict(
    name="bd2k-python-lib",
    version="1.13",

    author='Hannes Schmidt',
    author_email='hannes@ucsc.edu',
    url='https://github.com/BD2KGenomics/bd2k-python-lib',
    description='The BD2K Python module kitchen sink',

    package_dir={ '': 'src' },
    packages=find_packages( 'src' ),
    install_requires=[ ],
    tests_require=[
        'pytest==2.7.2',
        'mock==1.0.1',
        'lockfile==0.11.0',
        'boto==2.38.0' ],
    namespace_packages=[ 'bd2k' ] )

from setuptools.command.test import test as TestCommand


class PyTest( TestCommand ):
    user_options = [ ('pytest-args=', 'a', "Arguments to pass to py.test") ]

    def initialize_options( self ):
        TestCommand.initialize_options( self )
        self.pytest_args = [ ]

    def finalize_options( self ):
        TestCommand.finalize_options( self )
        self.test_args = [ ]
        self.test_suite = True

    def run_tests( self ):
        import pytest
        # Sanitize command line arguments to avoid confusing Toil code attempting to parse them
        sys.argv[ 1: ] = [ ]
        errno = pytest.main( self.pytest_args )
        sys.exit( errno )


kwargs[ 'cmdclass' ] = { 'test': PyTest }

setup( **kwargs )
