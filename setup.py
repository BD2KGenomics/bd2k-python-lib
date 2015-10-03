from setuptools import setup, find_packages

setup(
    name="bd2k-python-lib",
    version="1.8.dev2",

    author='Hannes Schmidt',
    author_email='hannes@ucsc.edu',
    url='https://github.com/BD2KGenomics/bd2k-python-lib',
    description='The BD2K Python module kitchen sink',

    package_dir={ '': 'src' },
    packages=find_packages( 'src' ),
    install_requires=[ ],
    namespace_packages=[ 'bd2k' ]
)
