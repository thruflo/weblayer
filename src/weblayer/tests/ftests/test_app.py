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
        
    
    def test_get_argument_from_query_string(self):
        """ Get argument from the request query string.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self, *args):
                return self.get_argument('foo')
            
        
        
        mapping = [(r'/(.*)', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/?foo=bar')
        
        self.assertTrue(res.body == 'bar')
        
    
    def test_get_arguments_from_query_string(self):
        """ Get multiple values for a query string argument.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self, *args):
                return ' '.join(self.get_arguments('foo'))
            
        
        
        mapping = [(r'/(.*)', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/?foo=bar&foo=bar&foo=blacksheep')
        
        self.assertTrue(res.body == 'bar bar blacksheep')
        
    
    def test_get_argument_from_query_string_with_multiple_values(self):
        """ Get argument from a query string with multiple values.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self, *args):
                return self.get_argument('foo')
            
        
        
        mapping = [(r'/(.*)', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/?foo=bar&foo=bar&foo=blacksheep')
        
        self.assertTrue(res.body == 'blacksheep')
        
    
    
