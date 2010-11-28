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
        """
        """
        
        self.context = Mock()
        self.context.response = Mock()
        self.context.settings = dict()
        self.context.settings['cookie_secret'] = ''
        self.cookie_wrapper = SecureCookieWrapper(self.context)
        
    
    def test_set(self):
        """
        """
        
        self.cookie_wrapper.set('name', 'value', timestamp='1')
        self.context.response.set_cookie.assert_called_with(
            'name',
            value='dmFsdWU=|1|7bcc09ebef2f6c967201709ed3cbeac3e4cb2872',
            max_age=2592000
        )
        
    
    


class TestGetCookie(unittest.TestCase):
    """ 
    """
    
    def setUp(self):
        """
        """
        
    
    
    def test_get(self):
        """
        """
        
    
    

