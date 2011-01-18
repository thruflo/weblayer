#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Functional tests for :py:mod:`~weblayer.examples.helloworld`.
"""

import unittest

class TestHelloWorld(unittest.TestCase):
    """ Sanity check the hello world example.
    """
    
    def make_app(self):
        from webtest import TestApp
        from weblayer.examples.helloworld import application
        return TestApp(application)
        
    
    def test_hello_world(self):
        """ Can we hook up a request handler with a positional argument
          from the request path and return a simple response?
        """
        
        app = self.make_app()
        res = app.get('/world')
        
        self.assertTrue(res.body == 'hello world')
        
    
    

