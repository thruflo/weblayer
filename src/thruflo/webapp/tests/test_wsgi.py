#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for `thruflo.webapp.wsgi`.
"""

import unittest
from mock import Mock

import thruflo.webapp.wsgi

class TestInitApplication(unittest.TestCase):
    """ Test the logic of `Application.__init__`.
    """
    
    def setUp(self):
        # monkey patch the component registry
        mock_registry = Mock()
        mock_registry.getUtility = Mock()
        mock_registry.getUtility.return_value = 42
        thruflo.webapp.wsgi.registry = mock_registry
        # monkey patch the `Request` and `Response` classes
        thruflo.webapp.wsgi.Request = 42
        thruflo.webapp.wsgi.Response = 42
        
    
    def test_path_router(self):
        """ If `path_router` is not None, it's available as 
          `self._path_router`.
        """
        
        app = thruflo.webapp.wsgi.Application(path_router=42)
        self.assertTrue(app._path_router == 42)
        
        app = thruflo.webapp.wsgi.Application(path_router='elephants')
        self.assertTrue(app._path_router == 'elephants')
        
    
    def test_path_router_from_registry(self):
        """ If `path_router` is None, which is the default, 
          `self._path_router` is looked up via the component registry.
        """
        
        
        
        app = thruflo.webapp.wsgi.Application()
        self.assertTrue(app._path_router == 42)
        
        app = thruflo.webapp.wsgi.Application(path_router=None)
        self.assertTrue(app._path_router == 42)
        
    
    def test_request_class(self):
        """ If `request_class` is not None, it's available as 
          `self._Request`.
        """
        
        app = thruflo.webapp.wsgi.Application(request_class=42)
        self.assertTrue(app._Request == 42)
        
        app = thruflo.webapp.wsgi.Application(request_class='elephants')
        self.assertTrue(app._Request == 'elephants')
        
    
    def test_request_class_from_base(self):
        """ If `request_class` is None, which is the default, 
          `self._Request` defaults to `base.Request`.
        """
        
        app = thruflo.webapp.wsgi.Application()
        self.assertTrue(app._Request == 42)
        
        app = thruflo.webapp.wsgi.Application(request_class=None)
        self.assertTrue(app._Request == 42)
        
    
    def test_response_class(self):
        """ If `response_class` is not None, it's available as 
          `self._Response`.
        """
        
        app = thruflo.webapp.wsgi.Application(response_class=42)
        self.assertTrue(app._Response == 42)
        
        app = thruflo.webapp.wsgi.Application(response_class='elephants')
        self.assertTrue(app._Response == 'elephants')
        
    
    def test_response_class_from_base(self):
        """ If `response_class` is None, which is the default, 
          `self._Response` defaults to `base.Response`.
        """
        
        app = thruflo.webapp.wsgi.Application()
        self.assertTrue(app._Response == 42)
        
        app = thruflo.webapp.wsgi.Application(request_class=None)
        self.assertTrue(app._Response == 42)
        
    
    def test_content_type(self):
        """ If `self._content_type' defalts to 'text/html; charset=UTF-8'
          unless `default_content_type` is passed in.
        """
        
        app = thruflo.webapp.wsgi.Application()
        self.assertTrue(app._content_type == 'text/html; charset=UTF-8')
        
        app = thruflo.webapp.wsgi.Application(default_content_type='elephants')
        self.assertTrue(app._content_type == 'elephants')
        
    
    

class TestCallApplication(unittest.TestCase):
    """ Test the logic of `Application.__call__`.
    """
    
    def setUp(self):
        self.environ = {'REQUEST_METHOD': 'FOO'}
        self.handler_class = Mock()
        self.handler_instance = Mock()
        self.handler_response = Mock()
        self.handler_response.return_value = 'handler response'
        self.handler_instance.return_value = self.handler_response
        self.handler_class.return_value = self.handler_instance
        self.path_router = Mock()
        self.path_router.match = Mock()
        self.path_router.match.return_value = (self.handler_class, ('a', 'b',))
        self.Request = Mock()
        self.request_instance = Mock()
        self.request_instance.path = '/path'
        self.Request.return_value = self.request_instance
        self.Response = Mock()
        self.response_instance = Mock()
        self.response_instance.return_value = 'minimal response'
        self.Response.return_value = self.response_instance
        self.app = thruflo.webapp.wsgi.Application(
            path_router=self.path_router,
            request_class=self.Request,
            response_class=self.Response,
            default_content_type='content type'
        )
        
    
    def test_instantiate_request(self):
        """ `app._Request` is called with `environ`.
        """
        
        response = self.app(self.environ, 'start response')
        self.Request.assert_called_with(self.environ)
        
    
    def test_instantiate_response(self):
        """ `app._Response` is called with `status` and `content_type`.
        """
        
        response = self.app(self.environ, 'start response')
        self.Response.assert_called_with(
            status=200, 
            content_type='content type'
        )
        
    
    def test_path_router_match_called(self):
        """ `self._path_router.match` is called with `request.path`.
        """
        
        response = self.app(self.environ, 'start response')
        self.path_router.match.assert_called_with(self.request_instance.path)
        
    
    def test_path_router_no_match_404(self):
        """ When `self._path_router.match` returns `(None, None)`,
          `response.status` is set to 404.
        """
        
        self.path_router.match.return_value = (None, None)
        
        response = self.app(self.environ, 'start response')
        self.assertTrue(self.response_instance.status == 404)
        
    
    def test_path_router_no_match_returns_minimal_response(self):
        """ When `self._path_router.match` returns `(None, None)`,
          `response.status` is set to 404.
        """
        
        self.path_router.match.return_value = (None, None)
        
        response = self.app(self.environ, 'start response')
        self.assertTrue(response == 'minimal response')
        
    
    def test_handler_class_init_with_request_and_response(self):
        """ `handler` is initialised with `request` and `response`.
        """
        
        response = self.app(self.environ, 'start response')
        self.handler_class.assert_called_with(
            self.request_instance, 
            self.response_instance
        )
        
    
    def test_handler_instance_called_with_method_and_groups(self):
        """ `handler` is called with `environ['REQUEST_METHOD']` & `*groups`.
        """
        
        response = self.app(self.environ, 'start response')
        self.handler_instance.assert_called_with(
            'FOO', 
            'a', 
            'b'
        )
        
    
    def test_handler_instance_throws_exception_500(self):
        """ When calling the handler raises an exception, returns a
           `response.status` is set to 500.
        """
        
        def raise_exception(): # pragma: no coverage
            raise Exception
        
        self.handler_instance = raise_exception
        self.handler_class.return_value = self.handler_instance
        self.path_router.match.return_value = (self.handler_class, ('a', 'b',))
        
        response = self.app(self.environ, 'start response')
        self.assertTrue(self.response_instance.status == 500)
        
    
    def test_handler_instance_throws_exception_returns_minimal_response(self):
        """ When calling the handler raises an exception, returns a
          minimal response.
        """
        
        def raise_exception(): # pragma: no coverage
            raise Exception
        
        self.handler_instance = raise_exception
        self.handler_class.return_value = self.handler_instance
        self.path_router.match.return_value = (self.handler_class, ('a', 'b',))
        
        response = self.app(self.environ, 'start response')
        self.assertTrue(response == 'minimal response')
        
    
    def test_handler_response_called(self):
        """ If all goes well, the handler response should be called
          with `self.environ` and 'start response'.
        """
        
        response = self.app(self.environ, 'start response')
        self.handler_response.assert_called_with(
            self.environ, 
            'start response'
        )
        
    
    def test_returns_called_handler_response(self):
        """ If all goes to plan, returns the called handler response.
        """
        
        response = self.app(self.environ, 'start response')
        self.assertTrue(response == 'handler response')
        
    
    

