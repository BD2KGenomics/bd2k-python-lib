from setuptools import setup, find_packages

setup(
    name="bd2k-python-lib",
    version="1.10.dev1",

    author='Hannes Schmidt',
    author_email='hannes@ucsc.edu',
    url='https://github.com/BD2KGenomics/bd2k-python-lib',
    description='The BD2K Python module kitchen sink',

    package_dir={ '': 'src' },
    packages=find_packages( 'src' ),
    install_requires=[ ],
    tests_require=[
        'mock==1.0.1' ],
    namespace_packages=[ 'bd2k' ] )
