#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import unittest
from mock import Mock

from thruflo.webapp.cookie import SecureCookieWrapper

class TestSetCookie(unittest.TestCase):
    """ 
    """
    
    def setUp(self):
        self.context = Mock()
        self.context.response = Mock()
        self.context.settings = dict()
        self.context.settings['cookie_secret'] = ''
        self.cookie_wrapper = SecureCookieWrapper(self.context)
        
    
    def test_name(self):
        """ Setting the cookie calls `self.context.response.set_cookie`
          with the 'name' as the first argument.
        """
        
        self.cookie_wrapper.set('name', 'value')
        args = self.context.response.set_cookie.call_args[0]
        self.assertTrue(args[0] == 'name')
        
    
    def test_name_is_basestring(self):
        """ The cookie name must be a basestring.
        """
        
        errs = (ValueError, TypeError)
        self.assertRaises(errs, self.cookie_wrapper.set, 0, 'value')
        
    
    def test_value(self):
        """ Setting the cookie runs the value through 
          `base64.b64encode` and puts into a '|' delimited string 
          with timestamp and hmac signature.
        """
        
        self.cookie_wrapper.set('name', 'value', timestamp='1')
        kwargs = self.context.response.set_cookie.call_args[1]
        value = 'dmFsdWU=|1|7bcc09ebef2f6c967201709ed3cbeac3e4cb2872'
        self.assertTrue(kwargs['value'] == value)
        
    
    def test_value_is_basestring(self):
        """ The cookie value must be a basestring.
        """
        
        errs = (ValueError, TypeError)
        self.assertRaises(errs, self.cookie_wrapper.set, 'name', 0)
        
    
    def test_expires_days(self):
        """ `expires_days` gets converted from days into seconds 
          and passed through as the `max_age`.
        """
        
        self.cookie_wrapper.set('name', 'value', expires_days=5)
        kwargs = self.context.response.set_cookie.call_args[1]
        five_days_as_seconds = 5 * 24 * 60 * 60
        self.assertTrue(kwargs['max_age'] == five_days_as_seconds)
        
    
    def test_expires_days_is_none(self):
        """ If the `expires_days` keyword argument is `None`,
          `max_age` is `None`.
        """
        
        self.cookie_wrapper.set('name', 'value', expires_days=None)
        kwargs = self.context.response.set_cookie.call_args[1]
        self.assertTrue(kwargs['max_age'] == None)
        
    
    def test_expires_days_is_int(self):
        """ If the `expires_days` keyword argument isn't `None` it
          must be an `int`.
        """
        
        self.cookie_wrapper.set('name', 'value', expires_days=None)
        kwargs = self.context.response.set_cookie.call_args[1]
        self.assertTrue(kwargs['max_age'] == None)
        self.assertRaises(
            TypeError,
            self.cookie_wrapper.set, 
            'name',
            'value',
            expires_days='30'
        )
        
    
    def test_kwargs(self):
        """ Other kwargs are passed through to 
          `self.context.response.set_cookie`,
        """
        
        self.cookie_wrapper.set('name', 'value', foo='bar')
        kwargs = self.context.response.set_cookie.call_args[1]
        self.assertTrue(kwargs['foo'] == 'bar')
        
    
    

class TestGetCookie(unittest.TestCase):
    """ 
    """
    
    def setUp(self):
        """
        """
        
        self.context = Mock()
        self.context.settings = dict()
        self.context.settings['cookie_secret'] = ''
        self.cookie_wrapper = SecureCookieWrapper(self.context)
        
    
    def test_get_name(self):
        """ Calling `get('name')` tries to get the value from
          `self.context.request.cookies`.
        """
        
        self.context.request.cookies = Mock()
        self.context.request.cookies.get.return_value = None
        self.cookie_wrapper.get('name')
        self.context.request.cookies.get.assert_called_with('name', None)
        
    
    def test_not_present(self):
        """ If the cookie doesn't exist, returns `None`.
        """
        
        self.context.request.cookies.get.return_value = None
        self.assertTrue(self.cookie_wrapper.get('name') is None)
        
    
    def test_split_value(self):
        """ If the cookie value doesn't split into three parts,
          delimited by returns `None`.
        """
        
        value = Mock()
        value.__len__ = Mock()
        value.split.return_value = ['a', 'b']
        result = self.cookie_wrapper.get('name', value=value)
        value.split.assert_called_with("|")
        self.assertTrue(result is None)
        
    
    
    # @@ ...
    

