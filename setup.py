from setuptools import setup, find_packages

setup(
    name = 'thruflo.webapp',
    version = '0.1',
    description = 'Yet another WSGI web app framework',
    long_description = open('README.md').read(),
    author = 'James Arthur',
    author_email = 'thruflo@googlemail.com',
    url = 'http://github.com/thruflo/thruflo.webapp',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Programming Language :: Python'
    ],
    license = open('LICENSE.md').read(),
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
        'setuptools_git==0.3.4',
        'simplejson>=2.0.9',
        'Mako>=0.3.2',
        'Beaker>=1.5.3',
        'redis>=1.34',
        'webob>=0.9.8',
        'pytz'
    ],
    entry_points = {
        'setuptools.file_finders': [
            "foobar = setuptools_git:gitlsfiles"
        ],
        'console_scripts': [
            'thruflo-webapp-demo = thruflo.webapp.demo.app:main'
        ]
    }
)