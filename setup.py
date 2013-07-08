#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


README = read('README.markdown')


setup(
    name='django-modeltools',
    version='0.1',
    description='A collection of utilities that make dealing with Django models more fun.',
    url='https://github.com/hzdg/django-modeltools',
    long_description=README,
    packages=find_packages(),
)
