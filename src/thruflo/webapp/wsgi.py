#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `WSGIApplication`_ implementation.
  
  .. _`WSGIApplication`: http://pythonpaste.org/
"""

__all__ = [
    'Application'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import IURLMapping, IWSGIApplication
from web import Request, Response

class WSGIApplication(object):
    """ Implementation of a callable WSGI application
      that uses a URL mapping to pass requests on.
    """
    
    adapts(IURLMapping)
    implements(IWSGIApplication)
    
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
          500 response.
          
          If no match is found, returns a minimalist 404 response.
          
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
            try:
                response = handler(environ['REQUEST_METHOD'], *groups)
            except Exception, err:
                response.status = 500
        else: # to handle 404 nicely, define a catch all url handler
            response.status = 404
        
        return response(environ, start_response)
        
    
    

