#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" XSRF validation.
"""

__all__ = [
    'XSRFError',
    'XSRFValidator'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import ICookieWrapper, IAuthenticationManager
from interfaces import IRequestHandler, IXSRFValidator

from utils import xhtml_escape

class XSRFError(ValueError):
    """ Raised when xsrf validation fails.
    """
    


class XSRFValidator(object):
    """ Protects against XSS attacks.
    """
    
    adapts(IRequestHandler)
    implements(IXSRFValidator)
    
    def __init__(self, context, xhtml_escape=xhtml_escape):
        self.context = context
        self.cookies = ICookieWrapper(self.context)
        self.auth = IAuthenticationManager(self.context)
        self._xhtml_escape = xhtml_escape
        
    
    
    @property
    def token(self):
        """ The XSRF-prevention token for the current user/session.
        """
        
        if not hasattr(self, '_xsrf_token'):
            token = self.cookies.get('_xsrf')
            if not token:
                token = binascii.b2a_hex(uuid.uuid4().bytes)
                expires_days = 30 if self.auth.is_authenticated else None
                self.cookies.set('_xsrf', token, expires_days=expires_days)
            self._xsrf_token = token
        return self._xsrf_token
        
    
    @property
    def form_html(self):
        """ An HTML <input/> element to be included with all POST forms.
        """
        
        if not hasattr(self, '_xsrf_form_html'):
            v = self._xhtml_escape(self.token)
            tag = u'<input type="hidden" name="_xsrf" value="{}"/>'
            self._xsrf_form_html = tag.format(v)
        return self._xsrf_form_html
        
    
    
    def validate_request(self):
        """ Raise an `XSRFError` if the '_xsrf' argument isn't present
          or if it doesn't match the '_xsrf'.
        """
        
        if self.context.request.method != "POST":
            return None
        
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return
            
        request_token = self.context.get_argument('_xsrf', None)
        
        if request_token is None:
            raise XSRFError(u'`_xsrf` argument missing from POST')
        
        if self.token != request_token:
            raise XSRFError(u'XSRF cookie does not match POST argument')
        
    
    

