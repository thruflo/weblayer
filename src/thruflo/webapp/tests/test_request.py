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
    


from thruflo.webapp.interfaces import ISettings, ITemplateRenderer
from thruflo.webapp.interfaces import IAuthenticationManager
from thruflo.webapp.interfaces import ISecureCookieWrapper
from thruflo.webapp.interfaces import IMethodSelector, IResponseNormaliser

import thruflo.webapp.request

class TestInitApplication(unittest.TestCase):
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
        
    
    def test_requires_request_and_response(self):
        """ Must pass in `request` and `response`.
        """
        
        self.assertRaises(
            TypeError,
            thruflo.webapp.request.Handler
        )
        
    
    def test_adapts_request(self):
        """ `request` is available as `self.request`.
        """
        
        handler = thruflo.webapp.request.Handler('req', '')
        self.assertTrue(handler.request == 'req')
        
    
    def test_adapts_response(self):
        """ `response` is available as `self.response`.
        """
        
        handler = thruflo.webapp.request.Handler('', 'resp')
        self.assertTrue(handler.response == 'resp')
        
    
    def test_settings(self):
        """ If `settings` is not None, it's available as 
          `self.settings`.
        """
        
        handler = thruflo.webapp.request.Handler('', '', settings=42)
        self.assertTrue(handler.settings == 42)
        
    
    def test_settings_from_registry(self):
        """ If `settings` is None, which is the default, 
          `self.settings` is looked up via the component registry.
        """
        
        handler = thruflo.webapp.request.Handler('', '')
        
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getUtility, 
                ISettings
            )
        )
        self.assertTrue(handler.settings == 'utility')
        
        handler = thruflo.webapp.request.Handler('', '', settings=None)
        self.assertTrue(handler.settings == 'utility')
        
    
    def test_template_renderer(self):
        """ If `template_renderer` is not None, it's available as 
          `self.template_renderer`.
        """
        
        handler = thruflo.webapp.request.Handler('', '', template_renderer=42)
        self.assertTrue(handler.template_renderer == 42)
        
    
    def test_template_renderer_from_registry(self):
        """ If `template_renderer` is None, which is the default, 
          `self.template_renderer` is looked up via the component registry.
        """
        
        handler = thruflo.webapp.request.Handler('', '')
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getUtility, 
                ITemplateRenderer
            )
        )
        self.assertTrue(handler.template_renderer == 'utility')
        
        handler = thruflo.webapp.request.Handler(
            '', 
            '', 
            template_renderer=None
        )
        self.assertTrue(handler.template_renderer == 'utility')
        
    
    def test_authentication_manager_adapter(self):
        """ If `authentication_manager_adapter` is not None, it's called
          with `self` and the return value is available as `self.auth`.
        """
        
        handler = thruflo.webapp.request.Handler(
            '', 
            '', 
            authentication_manager_adapter=self.adapter
        )
        self.adapter.assert_called_with(handler)
        self.assertTrue(handler.auth == 'adapted')
        
    
    def test_authentication_manager_adapter_from_registry(self):
        """ If `authentication_manager_adapter` is None, which is the default,
          `self.auth` is looked up via the component registry.
        """
        
        handler = thruflo.webapp.request.Handler('', '')
        
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter,
                handler,
                IAuthenticationManager
            )
        )
        self.assertTrue(handler.auth == 'adapted from registry')
        
        handler = thruflo.webapp.request.Handler(
            '', 
            '', 
            authentication_manager_adapter=None
        )
        self.assertTrue(handler.auth == 'adapted from registry')
        
    
    def test_secure_cookie_wrapper_adapter(self):
        """ If `secure_cookie_wrapper_adapter` is not None, it's called
          with `self` and the return value is available as `self.cookies`.
        """
        
        handler = thruflo.webapp.request.Handler(
            '', 
            '', 
            secure_cookie_wrapper_adapter=self.adapter
        )
        self.adapter.assert_called_with(handler)
        self.assertTrue(handler.cookies == 'adapted')
        
    
    def test_secure_cookie_wrapper_adapter_from_registry(self):
        """ If `secure_cookie_wrapper_adapter` is None, which is the default,
          `self.cookies` is looked up via the component registry.
        """
        
        handler = thruflo.webapp.request.Handler('', '')
        
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter,
                handler,
                ISecureCookieWrapper
            )
        )
        self.assertTrue(handler.cookies == 'adapted from registry')
        
        handler = thruflo.webapp.request.Handler(
            '', 
            '',
            secure_cookie_wrapper_adapter=None
        )
        self.assertTrue(handler.cookies == 'adapted from registry')
        
    
    def test_method_selector_adapter(self):
        """ If `method_selector_adapter` is not None, it's called with `self`
          and the return value is available as `self._method_selector`.
        """
        
        handler = thruflo.webapp.request.Handler(
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
        
        handler = thruflo.webapp.request.Handler('', '')
        
        self.assertTrue(
            _was_called_with(
                self.mock_registry.getAdapter,
                handler,
                IMethodSelector
            )
        )
        self.assertTrue(handler._method_selector == 'adapted from registry')
        
        handler = thruflo.webapp.request.Handler(
            '', 
            '', 
            method_selector_adapter=None
        )
        self.assertTrue(handler._method_selector == 'adapted from registry')
        
    
    def test_response_normaliser_adapter(self):
        """ `response_normaliser_adapter` defaults to None and is available
          as `self.response_normaliser_adapter`.
        """
        
        handler = thruflo.webapp.request.Handler('', '')
        self.assertTrue(handler._response_normaliser_adapter is None)
        
        handler = thruflo.webapp.request.Handler(
            '', 
            '',
            response_normaliser_adapter=42
        )
        self.assertTrue(handler._response_normaliser_adapter == 42)
        
    
    

