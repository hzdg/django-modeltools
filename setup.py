#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


README = read('README.rst')


setup(
    name='django-modeltools',
    version='1.0.1',
    author='HZDG',
    author_email='webmaster@hzdg.com',
    description='A collection of utilities that make dealing with Django models more fun.',
    license='MIT',
    url='https://github.com/hzdg/django-modeltools',
    long_description=README,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
