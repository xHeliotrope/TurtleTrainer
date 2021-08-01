#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='trainer',
    version='1.0',
    description='Bots Playing NES Games',
    author='Ryan Moore',
    packages=find_packages(exclude=['tests*']),
)
