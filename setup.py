# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    description = f.read()


setup(
    name='onghub',
    url='http://github.com/emulbreh/onghub/',
    version='0.1.0',
    packages=find_packages(),
    license=u'Apache 2',
    long_description=description,
    include_package_data=True,
    install_requires=[
        'itsdangerous',
        'Werkzeug',
        'gevent',
        'PyYAML',
    ],
    entry_points={
        'console_scripts': ['onghub = onghub.cli:main'],
    }
)
