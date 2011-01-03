from setuptools import setup

setup(
    name = 'weblayer-pastedemo',
    version = '0.1',
    install_requires=[
        'weblayer',
        'PasteScript',
        'WSGIUtils'
    ],
    scripts = ['demo.py'],
    entry_points = {
        'paste.app_factory': [
            'main=demo:app_factory',
        ]
    }
)
