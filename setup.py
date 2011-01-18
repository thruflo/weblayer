#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, join as join_path
from setuptools import setup, find_packages

def _get_long_description():
    sock = open('README.rst')
    long_description = sock.read()
    sock.close()
    return long_description
    


setup(
    name = 'weblayer',
    version = '0.3',
    description = 'A lightweight, componentised package for writing web applications',
    long_description = _get_long_description(),
    author = 'James Arthur',
    author_email = 'username: thruflo, domain: gmail.com',
    url = 'http://packages.python.org/weblayer',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Paste',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    license = 'http://creativecommons.org/publicdomain/zero/1.0/',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe = False,
    install_requires=[
        'zope.interface >= 3.6.1, < 4.0',
        'zope.component >= 3.10, < 4.0',
        'venusian >= 0.5, < 0.6',
        'webob >= 1.0, < 2.0',
        'Mako >= 0.3.6, < 0.4'
    ],
    extras_require = {
        'dev': [
            'WebTest >= 1.2.3, < 1.3',
            'nose >= 1.0, < 2.0',
            'coverage >= 3.4, < 4.0',
            'mock >= 0.7.0b4, < 0.8',
            'Sphinx >= 1.0.5, < 2.0',
            'repoze.sphinx.autointerface >= 0.4, < 0.5',
            'setuptools_git >= 0.3, < 0.4'
        ]
    },
    entry_points = {
        'setuptools.file_finders': [
            "foobar = setuptools_git:gitlsfiles"
        ],
        'console_scripts': [
            'weblayer-demo = weblayer.examples.helloworld:main'
        ]
    }
)
