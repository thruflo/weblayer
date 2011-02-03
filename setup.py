#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, join as join_path
from setuptools import setup, find_packages

def _read(file_name):
    sock = open(file_name)
    text = sock.read()
    sock.close()
    return text
    


setup(
    name = 'weblayer',
    version = '0.4.3',
    description = 'A lightweight, componentised package for writing web applications',
    long_description = _read('README.rst'),
    author = 'James Arthur',
    author_email = 'username: thruflo, domain: gmail.com',
    url = 'http://packages.python.org/weblayer',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license = 'http://unlicense.org/UNLICENSE',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe = False,
    install_requires=[
        'WebOb==1.0.1',
        'Mako==0.3.6',
        'venusian==0.5',
        'zope.interface==3.6.1',
        'zope.component==3.10.0',
        'setuptools-git==0.3.4'
    ],
    extras_require = {
        'dev': [
            'coverage==3.4',
            'nose==1.0.0',
            'mock==0.7.0b4',
            'repoze.sphinx.autointerface==0.4',
            'Sphinx==1.0.7',
            'WebTest==1.2.3'
        ]
    },
    entry_points = {
        'setuptools.file_finders': [
            "foobar = setuptools_git:gitlsfiles"
        ],
        'console_scripts': [
            "weblayer-demo = weblayer.examples.helloworld:main"
        ]
    }
)
