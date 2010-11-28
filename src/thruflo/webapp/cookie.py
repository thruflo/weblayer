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

require_setting('cookie_secret', help='a long, random sequence of bytes')

class SecureCookieWrapper(object):
    """ Adapts a request handler to provide methods to get 
      and set cookies that can't be forged.
    """
    
    adapts(IRequestHandler)
    implements(ICookieWrapper)
    
    def __init__(self, context, digestmod=hashlib.sha1):
        self.context = context
        self._cookie_secret = self.context.settings['cookie_secret']
        self._digestmod = digestmod
    
    def _generate_cookie_signature(self, *parts):
        """ Generate a secure cookie signature.
        """
        
        hasher = hmac.new(self._cookie_secret, digestmod=self._digestmod)
        for part in parts:
            hasher.update(part)
        return hasher.hexdigest()
        
    
    def set(self, name, value, expires_days=30, **kwargs):
        """ Signs and timestamps a cookie so it cannot be forged.
        """
        
        timestamp = str(int(time.time()))
        value = base64.b64encode(value)
        signature = self._generate_cookie_signature(name, value, timestamp)
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
        
        if include_name:
            signature = self._generate_cookie_signature(name, parts[0], parts[1])
        else:
            signature = self._generate_cookie_signature(parts[0], parts[1])
        
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

        self.response.set_cookie(
            name, 
            '', 
            path=path, 
            domain=domain, 
            max_age=0, 
            expires=datetime.timedelta(days=-5)
        )




    
    
    

