#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGES.rst') as history_file:
    history = history_file.read()

requirements = [
    "blinker",
    "jaraco.classes>=1.1",
    "pika",
    "PikaChewie>=1.3",
    "six",
]

setup(
    name='yg.emanate',
    version='0.4.0',
    description="Lightweight event system for Python",
    long_description=readme + '\n\n' + history,
    author="YouGov, plc",
    author_email='dev@yougov.com',
    url='https://github.com/yougov/yg.emanate',
    packages=[
        'yg.emanate',
    ],
    namespace_packages=['yg'],
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='emanate',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
)
