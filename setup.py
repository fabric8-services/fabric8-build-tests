#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'pytest',
    'requests',
    'jq',
]

setup_requirements = [
    'pytest-runner',
]

setup(
    name='fabric8_build_tests',
    version='0.1.0',
    description="Integration tests for Fabric8 build service",
    long_description=readme,
    author="Sunil Thaha",
    author_email='3005132+sthaha@users.noreply.github.com',
    url='https://github.com/fabric8-services/fabric8-build-tests',
    packages=find_packages(include=['tests']),
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='fabric8_build_tests',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    setup_requires=setup_requirements,
)
