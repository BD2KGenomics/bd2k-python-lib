from setuptools import setup, find_packages

setup(
    name="bd2k-python-lib",
    version="1.5.dev1",
    package_dir={ '': 'src' },
    packages=find_packages( 'src' ),
    install_requires=[ ],
    namespace_packages=[ 'bd2k' ]
)
