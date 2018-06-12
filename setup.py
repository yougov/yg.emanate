#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='yg.emanate',
    use_scm_version=True,
    description="Lightweight event system for Python",
    author="YouGov, plc",
    author_email='dev@yougov.com',
    url='https://github.com/yougov/yg.emanate',
    packages=[
        'yg.emanate',
    ],
    namespace_packages=['yg'],
    include_package_data=True,
    setup_requires=['setuptools_scm>=1.15'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
)
