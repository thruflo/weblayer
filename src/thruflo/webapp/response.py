#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Response normalising.
"""

__all__ = [
    'DefaultToJSONResponseNormaliser'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequestHandler, IResponseNormaliser
from utils import json_encode

class DefaultToJSONResponseNormaliser(object):
    """ Adapter to normalise the response from a 
      request handler method.
    """
    
    adapts(IRequestHandler)
    implements(IResponseNormaliser)
    
    def __init__(
            self, 
            context, 
            json_content_type='application/json; charset=UTF-8',
            json_encode=json_encode
        ):
        self.context = context
        self._json_content_type = json_content_type
        self._json_encode = json_encode
        
    
    
    def normalise(self, handler_response):
        """ If `handler_response` implements `IResponse` then
          just use that::
          
              >>> # @@
              
          Otherwise if it's a `str` or a `unicode` use that
          as the response body::
          
              >>> # @@
              
          If it's `None` then do nothing::
          
              >>> # @@
          
          Otherwise (with this particular implementation) assume
          we want to encode `handler_response` as a json string
          as use that as the response body::
          
              >>> # @@
          
        """
        
        if IResponse.providedBy(handler_response):
            self.context.response = handler_response
        elif isinstance(handler_response, str):
            self.context.response.body = handler_response
        elif isinstance(handler_response, unicode):
            self.context.response.unicode_body = handler_response
        elif handler_response is None: # leave self.response alone
            pass
        else: # assume it's json data
            self.context.response.content_type = self._json_content_type
            self.context.response.unicode_body = self._json_encode(handler_response)
        
        return self.context.response
        
    
    

