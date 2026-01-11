# -*- coding: utf-8 -*-
"""
Versioning
Proper versioning is essential for wheels. Follow a semantic versioning
scheme (e.g., MAJOR.MINOR.PATCH). When making backward-incompatible changes,
increment the MAJOR version. For backward-compatible new features,
increment the MINOR version, and for bug fixes, increment the PATCH version.

Python Packaging User Guide https://packaging.python.org/en/latest/
setuptools Documentation https://setuptools.pypa.io/en/latest/
wheel Documentation https://wheel.readthedocs.io/en/stable/

Created on Sun Jan 11 10:16:58 2026.

@author: Bob
"""

from setuptools import setup, find_packages

setup(
    name='NGS_CD_Reader',
    version='1.0.0',
    packages=find_packages(),
    author='Robert Bumpous',
    author_email='BBFlyer1@comcast.net',
    description='''A Python package to read the first 100 years of National
    Geographic Society magazines from their CD Set.
    ''',
)