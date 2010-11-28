#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Secure cookie wrapper.
"""

__all__ = [
    'SecureCookieWrapper'
]

import base64
import datetime
import hashlib
import hmac
import time

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequestHandler, ICookieWrapper
from settings import require_setting
from utils import encode_to_utf8

require_setting('cookie_secret', help='a long, random sequence of bytes')

def _time_independent_equals(a, b):
    """
    """
    
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    
    return result == 0
    

def _generate_cookie_signature(cookie_secret, *parts):
    """ Generate a secure cookie signature::
      
          >>> cookie_secret = ''
          >>> _generate_cookie_signature(cookie_secret)
          'fbdb1d1b18aa6c08324b7d64b71fb76370690e1d'
      
      All args after the first are passed to the hasher and must
      be str or unicode, with the unicode being encoded to utf-8::
      
          >>> parts = ['a', 'b', 'c']
          >>> _generate_cookie_signature(cookie_secret, *parts)
          '9b4a918f398d74d3e367970aba3cbe54e4d2b5d9'
          >>> parts.append(u'd')
          >>> _generate_cookie_signature(cookie_secret, *parts)
          'afa29ab8534495251ac8346a985717c54bc49c26'
          >>> parts.append([])
          >>> _generate_cookie_signature(cookie_secret, *parts) #doctest:+ELLIPSIS
          Traceback (most recent call last):
          ...
          ValueError: [] must be a `basestring`
      
    """
    
    hasher = hmac.new(cookie_secret, digestmod=hashlib.sha1)
    
    parts = [encode_to_utf8(part) for part in parts]
    for part in parts:
        hasher.update(part)
    
    return hasher.hexdigest()
    


class SecureCookieWrapper(object):
    """ Adapts a request handler to provide methods to get 
      and set cookies that can't be forged.
    """
    
    adapts(IRequestHandler)
    implements(ICookieWrapper)
    
    def __init__(self, context):
        self.context = context
        self._cookie_secret = self.context.settings['cookie_secret']
        
    
    def set(self, name, value, timestamp=None, expires_days=30, **kwargs):
        """ Signs and timestamps a cookie so it cannot be forged.
        """
        
        timestamp = timestamp and timestamp or str(int(time.time()))
        value = base64.b64encode(value)
        args = (name, value, timestamp)
        signature = _generate_cookie_signature(self._cookie_secret, *args)
        value = "|".join([value, timestamp, signature])
        
        max_age = None
        if expires_days:
            max_age = expires_days * 24 * 60 * 60
        
        return self.context.response.set_cookie(
            name, 
            value=value, 
            max_age=max_age, 
            **kwargs
        )
        
    
    def get(self, name, include_name=True, value=None):
        """ Returns the given signed cookie if it validates, or None.
        """
        
        if value is None: 
            value = self.request.cookies.get(name, None)
        
        if not value:
            return None
        
        parts = value.split("|")
        if len(parts) != 3: 
            return None
        
        args = include_name and (name, parts[0], parts[1]) or (parts[0], parts[1])
        signature = _generate_cookie_signature(self._cookie_secret, *args)
        
        if not _time_independent_equals(parts[2], signature):
            logging.warning("Invalid cookie signature %r", value)
            return None
        
        timestamp = int(parts[1])
        if timestamp < time.time() - 31 * 86400:
            logging.warning("Expired cookie %r", value)
            return None
        
        try:
            return base64.b64decode(parts[0])
        except:
            return None
        
    
    def delete(self, name, path="/", domain=None):
        """ Convienience method to clear a cookie.
        """
        
        self.context.response.set_cookie(
            name, 
            '', 
            path=path, 
            domain=domain, 
            max_age=0, 
            expires=datetime.timedelta(days=-5)
        )
        
    
    

