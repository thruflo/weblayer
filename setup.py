#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'thruflo.webapp',
    version = '0.2',
    description = 'Minimal, testable WSGI framework',
    long_description = open('README.rst').read(),
    author = 'James Arthur',
    author_email = 'thruflo@geemail.com',
    url = 'http://github.com/thruflo/thruflo.webapp',
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
    namespace_packages = [
        'thruflo'
    ],
    package_dir = {
        '': 'src'
    },
    include_package_data = True,
    zip_safe = False,
    install_requires=[
        'zope.interface >= 3.6, < 4.0',
        'zope.component >= 3.10, < 4.0',
        'venusian', # ' >= 4.0, < 5.0',
        'webob >= 1.0, < 2.0',
        'Mako >= 0.3, < 0.4'
    ],
    extras_require = {
        'dev': [
            'setuptools_git >= 0.3, < 0.4'
        ],
        'tests': [
            'nose >= 0.11, < 1.0',
            'coverage >= 3.4, < 4.0',
            'mock >= 0.7, < 0.8'
        ],
        'docs': [
            'Sphinx >= 1.0, < 2.0',
            'repoze.sphinx.autointerface >= 0.4, < 0.5'
        ]
    },
    entry_points = {
        'setuptools.file_finders': [
            "foobar = setuptools_git:gitlsfiles"
        ],
        'console_scripts': [
            'thruflo-webapp-demo = thruflo.webapp.demo.app:main'
        ]
    }
)