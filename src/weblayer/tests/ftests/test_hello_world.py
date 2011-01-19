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
        
    
    def test_main(self):
        """ ``def main()`` calls ``wsgiref.simple_server.make_server`` with
          ``''``, ``8080`` and ``weblayer.examples.helloworld.application``.
        """
        
        from weblayer.examples.helloworld import application, main
        
        # patch ``make_server``
        from mock import Mock
        import wsgiref.simple_server
        __make_server = wsgiref.simple_server.make_server
        mock_make_server = Mock()
        wsgiref.simple_server.make_server = mock_make_server
        
        main()
        mock_make_server.assert_called_with('', 8080, application)
        
        # restore ``make_server``
        wsgiref.simple_server.make_server = __make_server
        
    
    

