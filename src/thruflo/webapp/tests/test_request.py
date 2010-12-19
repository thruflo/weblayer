#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for `thruflo.webapp.request`.
"""

import unittest
from mock import Mock

def _was_called_with(m, *args, **kwargs):
    """ Takes a mock and the args and kwargs it should have been
      called with, iterates through the call_args_list and returns
      `True` if they match once.
      
          >>> m = Mock()
          >>> m1 = m('a', foo='bar')
          >>> m2 = m('b', baz='blah')
          >>> _was_called_with(m, 'b', baz='blah')
          True
          >>> _was_called_with(m, 'a', foo='bar')
          True
          >>> _was_called_with(m, 'a')
          False
          >>> _was_called_with(m, baz='blah')
          False
      
    """
    
    for item in m.call_args_list:
        if item[0] == args and item[1] == kwargs:
            return True
        
    return False
    


from thruflo.webapp.interfaces import IRequirableSettings, ITemplateRenderer
from thruflo.webapp.interfaces import IAuthenticationManager
from thruflo.webapp.interfaces import ISecureCookieWrapper
from thruflo.webapp.interfaces import IMethodSelector, IResponseNormaliser

import thruflo.webapp.request
from thruflo.webapp.request import Handler

class TestInitHandler(unittest.TestCase):
    """ Test the logic of `Handler.__init__`.
    """
    
    def setUp(self):
        """ Monkey patch the component registry.
        """
        
        self.adapter = Mock()
        self.adapter.return_value = 'adapted'
        self.mock_registry = Mock()
        self.mock_registry.getUtility = Mock()
        self.mock_registry.getUtility.return_value = 'utility'
        self.mock_registry.getAdapter = Mock()
        self.mock_registry.getAdapter.return_value = 'adapted from registry'
        thruflo.webapp.request.registry = self.mock_registry
        
    
    def test_requires_args(self):
        """ Must pass in `request`, `response` and `settings`.
        """
        
        self.assertRaises(
            TypeError,
            Handler
        )
        self.assertRaises(
            TypeError,
            Handler,
            ''
        )
        self.assertRaises(
            TypeError,
            Handler,
            '',
            ''
        )
        
    
    def test_adapts_request(self):
        """ `request` is available as `self.request`.
        """
        
        handler = Handler('req', '', '')
        self.assertTrue(handler.request == 'req')
        
    
    def test_adapts_response(self):
        """ `response` is available as `self.response`.
        """
        
        handler = Handler('', 'resp', '')
        self.assertTrue(handler.response == 'resp')
        
    
    def test_adapts_settings(self):
        """ `settings` is available as self.settings`.
        """
        
        handler = Handler('', '', 'settings')
        self.assertTrue(handler.settings == 'settings')
        
    
    def test_template_renderer_adapter(self):
        """ If `template_renderer_adapter` is not None, it's called with
          `self.settings` and the return value is available as 
          `self.template_renderer`.
        """
        
        handler = Handler(
            '', 
            '', 
            '',
            template_renderer_adapter=self.adapter
        )
        self.adapter.assert_called_with(handler.settings)
        self.assertTrue(handler.template_renderer == 'adapted')
        
    
    def test_template_renderer_adapter_from_registry(self):
        """ If `template_renderer` is None, which is the default, 
          `self.template_renderer` is looked up via the component registry.
        """
        
        handler = Handler('', '', '')
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter, 
                '',
                ITemplateRenderer
            )
        )
        self.assertTrue(handler.template_renderer == 'adapted from registry')
        
        handler = Handler(
            '', 
            '', 
            '', 
            template_renderer_adapter=None
        )
        self.assertTrue(handler.template_renderer == 'adapted from registry')
        
    
    def test_authentication_manager_adapter(self):
        """ If `authentication_manager_adapter` is not None, it's called
          with `self.request` and the return value is available as `self.auth`.
        """
        
        handler = Handler(
            '', 
            '', 
            '',
            authentication_manager_adapter=self.adapter
        )
        self.adapter.assert_called_with(handler.request)
        self.assertTrue(handler.auth == 'adapted')
        
    
    def test_authentication_manager_adapter_from_registry(self):
        """ If `authentication_manager_adapter` is None, which is the default,
          `self.auth` is looked up via the component registry.
        """
        
        handler = Handler('', '', '')
        
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter,
                handler.request,
                IAuthenticationManager
            )
        )
        self.assertTrue(handler.auth == 'adapted from registry')
        
        handler = Handler(
            '', 
            '', 
            '', 
            authentication_manager_adapter=None
        )
        self.assertTrue(handler.auth == 'adapted from registry')
        
    
    def test_secure_cookie_wrapper_adapter(self):
        """ If `secure_cookie_wrapper_adapter` is not None, it's called
          with `self` and the return value is available as `self.cookies`.
        """
        
        handler = Handler(
            '', 
            '', 
            '', 
            secure_cookie_wrapper_adapter=self.adapter
        )
        self.adapter.assert_called_with(
            handler.request, 
            handler.response, 
            handler.settings
        )
        self.assertTrue(handler.cookies == 'adapted')
        
    
    def test_secure_cookie_wrapper_adapter_from_registry(self):
        """ If `secure_cookie_wrapper_adapter` is None, which is the default,
          `self.cookies` is looked up via the component registry.
        """
        
        handler = Handler('', '', '')
        
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter,
                handler.request, 
                handler.response, 
                handler.settings,
                ISecureCookieWrapper
            )
        )
        self.assertTrue(handler.cookies == 'adapted from registry')
        
        handler = Handler(
            '', 
            '', 
            '', 
            secure_cookie_wrapper_adapter=None
        )
        self.assertTrue(handler.cookies == 'adapted from registry')
        
    
    def test_method_selector_adapter(self):
        """ If `method_selector_adapter` is not None, it's called with `self`
          and the return value is available as `self._method_selector`.
        """
        
        handler = Handler(
            '', 
            '', 
            '', 
            method_selector_adapter=self.adapter
        )
        self.adapter.assert_called_with(handler)
        self.assertTrue(handler._method_selector == 'adapted')
        
    
    def test_method_selector_adapter_from_registry(self):
        """ If `method_selector_adapter` is None, which is the default,
          `self.auth` is looked up via the component registry.
        """
        
        handler = Handler('', '', '')
        
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter,
                handler,
                IMethodSelector
            )
        )
        self.assertTrue(handler._method_selector == 'adapted from registry')
        
        handler = Handler(
            '', 
            '', 
            '', 
            method_selector_adapter=None
        )
        self.assertTrue(handler._method_selector == 'adapted from registry')
        
    
    def test_response_normaliser_adapter(self):
        """ `response_normaliser_adapter` defaults to None and is available
          as `self.response_normaliser_adapter`.
        """
        
        handler = Handler('', '', '')
        self.assertTrue(handler._response_normaliser_adapter is None)
        
        handler = Handler(
            '', 
            '', 
            '', 
            response_normaliser_adapter=42
        )
        self.assertTrue(handler._response_normaliser_adapter == 42)
        
    
    

class TestHandlerMethods(unittest.TestCase):
    """ Test the logic of `Handler` methods.
    """
    
    def setUp(self):
        self.request = Mock()
        self.response = Mock()
        self.settings = {}
        self.template_renderer_adapter = Mock()
        self.static_url_generator_adapter = Mock()
        self.authentication_manager_adapter = Mock()
        self.secure_cookie_wrapper_adapter = Mock()
        self.method_selector_adapter = Mock()
        self.handler = Handler(
            self.request,
            self.response,
            self.settings,
            template_renderer_adapter=self.template_renderer_adapter,
            static_url_generator_adapter=self.static_url_generator_adapter,
            authentication_manager_adapter=self.authentication_manager_adapter,
            secure_cookie_wrapper_adapter=self.secure_cookie_wrapper_adapter,
            method_selector_adapter=self.method_selector_adapter
        )
        
    
    
    def test_get_argument_calls_get_arguments(self):
        """ `get_argument` calls `get_arguments` with `strip` defaulting to
          `False`.
        """
        
        self.handler.get_arguments = Mock()
        self.handler.get_arguments.return_value = []
        self.handler.get_argument('foo')
        self.handler.get_arguments.assert_called_with('foo', strip=False)
        
    
    def test_get_argument_strip(self):
        """ `strip` is passed through.
        """
        
        self.handler.get_arguments = Mock()
        self.handler.get_arguments.return_value = []
        self.handler.get_argument('foo', strip=True)
        self.handler.get_arguments.assert_called_with('foo', strip=True)
        
    
    def test_get_argument_return_value(self):
        """ `get_argument` returns the last item from the list `get_arguments`
          returns.
        """
        
        self.handler.get_arguments = Mock()
        self.handler.get_arguments.return_value = ['a', 'b']
        self.assertTrue(self.handler.get_argument('foo') == 'b')
        
    
    def test_get_argument_default(self):
        """ Unless get_arguments returns `[]` in which case `get_argument`
          returns `default` which defaults to `None`.
        """
        
        self.handler.get_arguments = Mock()
        self.handler.get_arguments.return_value = []
        self.assertTrue(self.handler.get_argument('foo') is None)
        self.assertTrue(
            self.handler.get_argument('foo', default='abc') == 'abc'
        )
        
    
    
    def test_get_arguments_calls_get_arguments(self):
        """ `get_argument` calls `request.params.get`.
        """
        
        self.handler.get_arguments('foo')
        self.request.params.get.assert_called_with('foo', [])
        
    
    def test_get_arguments_calls_wraps_single_value(self):
        """ If `request.params.get` returns a single value, wraps it in 
          a `list`.
        """
        
        self.request.params.get.return_value = 'a'
        self.assertTrue(self.handler.get_arguments('foo') == ['a'])
        
    
    def test_get_arguments_calls_multiple_value(self):
        """ If `request.params.get` returns a list, returns it.
        """
        
        self.request.params.get.return_value = ['a', 'b']
        self.assertTrue(self.handler.get_arguments('foo') == ['a', 'b'])
        
    
    def test_get_arguments_doesnt_strip(self):
        """ Doesn't strip by default.
        """
        
        self.request.params.get.return_value = [' a ', ' b ']
        self.assertTrue(self.handler.get_arguments('foo') == [' a ', ' b '])
        
    
    def test_get_arguments_unless_told_to_strip(self):
        """ Strips if told to.
        """
        
        self.request.params.get.return_value = [' a ', ' b ']
        self.assertTrue(
            self.handler.get_arguments('foo', strip=True) == ['a', 'b']
        )
        
    
    

