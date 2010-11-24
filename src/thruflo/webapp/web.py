#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `WSGIApplication`_ and `RequestHandler` implementations.
  
  .. _`WSGIApplication`: http://pythonpaste.org/
"""

__all__ = [
    'RequestHandler',
    'WSGIApplication'
]

import datetime

import webob

from zope.component import adapts
from zope.interface import implements

from interfaces import *

class Request(webob.Request):
    """ We use `webob.Request` as our default
      `IRequest` implementation.
    """
    
    implements(IRequest)
    

class Response(webob.Response):
    """ We use `webob.Response` as our default
      `IResponse` implementation.
    """
    
    implements(IResponse)
    

class RequestHandler(object):
    """
    """
    
    adapts(IRequest, IResponse)
    implements(IRequestHandler)
    
    def __call__(self, method_name, *groups):
        
        # @@ lookup self.method and guard against random method names
        
        """
        if isinstance(handler_response, webob.Response):
            response = handler_response
        elif isinstance(handler_response, str):
            response.body = handler_response
        elif isinstance(handler_response, unicode):
            response.unicode_body = handler_response
        else: # assume it's data
            response.content_type = 'application/json; charset=UTF-8'
            response.unicode_body = utils.json_encode(handler_response)
        """
        
        # response = handler.handle_exception(err)
    
    

class WSGIApplication(object):
    """ Implementation of a callable WSGI application.
    """
    
    implements(IWSGIApplication)
    adapts(IURLMapping)
    
    def __init__(
            self,
            url_mapping,
            request_class=Request,
            response_class=Response,
            default_content_type='text/html; charset=UTF-8'
        ):
        self._url_mapping = url_mapping
        self._request_class = request_class
        self._response_class = response_class
        self._default_content_type = default_content_type
        
    
    def __call__(self, environ, start_response):
        """ Checks the url mapping for a match against the
          incoming request path.  If it finds one, instantiates
          the corresponding request handler and calls it with
          the request method and the match groups.
          
          If calling the handler errors, returns a minimalist
          500 response.  If no match is found, returns a 
          minimalist 404 response.
          
        """
        
        handler = None
        groups = ()
        
        request = self._request_class(environ)
        response = self._response_class(
            status=200, 
            content_type=self._default_content_type
        )
        
        for regexp, handler_class in self._url_mapping.mapping:
            match = regexp.match(request.path)
            if match:
                handler = handler_class(request, response)
                groups = match.groups()
                break
            
        if handler:
            method_name = environ['REQUEST_METHOD'].lower()
            try:
                response = handler(method_name, *groups)
            except Exception, err:
                response.status = 500
        else: # to handle 404 nicely, define a catch all url handler
            response.status = 404
        
        return response(environ, start_response)
        
    
    


"""
import utils
DEFAULT_BUILT_INS = {
    "escape": utils.xhtml_escape,
    "url_escape": utils.url_escape,
    "json_encode": utils.json_encode,
    "squeeze": utils.squeeze,
    "datetime": datetime,
}
"""
