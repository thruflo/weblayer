#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Functional tests for ...
"""

import unittest
from mock import Mock

class TestFoo(unittest.TestCase):
    """
    """
    
    def make_app(self, handler_class):
        
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        
        mapping = [(r'/(.*)', handler_class)]
        config = {
            'cookie_secret': '...', 
            'static_files_path': '/var/www/static',
            'template_directories': ['templates']
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        
        return TestApp(application)
        
    
    def test_paste_throw_errors_in_environ(self):
        
        from weblayer import RequestHandler
        
        class Hello(RequestHandler):
            def get(self, world):
                return u'hello %s' % world
            
        
        
        app = self.make_app(Hello)
        res = app.get('/')
        
        self.assertTrue(res.environ['paste.throw_errors'])
        
    
    
