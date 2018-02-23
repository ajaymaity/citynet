#!/usr/bin/python
# coding=utf-8
"""Main package management file for the backend python package."""
from setuptools import setup, find_packages
import unittest
import os


def all_tests():
    """Create a test suite with all files matching 'test/test_*.py'."""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite


docker_file = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "..", "docker", "requirements.txt")

# list the requirements from the docker path
with open(docker_file) as f:
        requirements = f.read().splitlines()


setup(
    name='cityback',
    version='0.1.0',
    packages=find_packages('cityback'),  # include all packages under src
    package_dir={'': 'cityback'},   # tell distutils packages are under src
    scripts=['bin/cityback_script.py'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    install_requires=requirements,
    description='Backend of the citynet project',
    test_suite="setup.all_tests"
)
