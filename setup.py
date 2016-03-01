#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "jsonschema"
    # TODO: put package requirements here
]

test_requirements = [
        "jsonschema"
    # TODO: put package test requirements here
]

setup(
    name='pycorm',
    version='0.2.13',
    description="a pico orm that uses jsonschema",
    long_description=readme + '\n\n' + history,
    author="Johannes Valbjørn",
    author_email='johannes.valbjorn@gmail.com',
    url='https://github.com/sloev/pycorm',
    packages=[
        'pycorm',
    ],
    package_dir={'pycorm':
                 'pycorm'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='pycorm',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
