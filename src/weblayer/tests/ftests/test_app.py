#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Functional tests for a :ref:`weblayer` application using the 
  :ref:`request handler api`.
"""

import unittest

class TestApplication(unittest.TestCase):
    
    def make_app(self, mapping):
        from os.path import dirname, join as join_path
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        _here = dirname(__file__)
        config = {
            'cookie_secret': 'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715d',
            'static_files_path': join_path(_here, 'static'),
            'template_directories': [join_path(_here, 'templates')]
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_hello_world(self):
        """ Should return `u'hello world'`.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self, world):
                return u'hello %s' % world
            
        
        
        mapping = [(r'/(.*)', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/world')
        
        self.assertTrue(res.body == 'hello world')
        
    
    def test_unicode_response(self):
        """ Should return `u'hello Ð'`.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self, *args):
                return u'hello Ð'
            
        
        
        mapping = [(r'/(.*)', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/')
        
        self.assertTrue(res.unicode_body == u'hello Ð')
        
    
    
