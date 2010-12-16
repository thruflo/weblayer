#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `WSGIApplication <http://pythonpaste.org/>`_ implementation.
"""

__all__ = [
    'WSGIApplication'
]

from zope.interface import implements

from base import Request, Response
from component import registry
from interfaces import IPathRouter, IWSGIApplication

class WSGIApplication(object):
    """ Implementation of a callable WSGI application that 
      accepts requests and uses a path router to select
      a request handler to handle them.
    
    """
    
    implements(IWSGIApplication)
    
    def __init__(
            self,
            path_router=None,
            request_class=None,
            response_class=None,
            default_content_type='text/html; charset=UTF-8'
        ):
        """
        """
        
        if path_router is None:
            self._path_router = registry.getUtility(IPathRouter)
        else:
            self._path_router = path_router
        
        if request_class is None:
            self._Request = Request
        else:
            self._Request = request_class
        
        if response_class is None:
            self._Response = Response
        else:
            self._Response = response_class
        
        self._content_type = default_content_type
        
    
    def __call__(self, environ, start_response):
        """ Checks the url mapping for a match against the
          incoming request path.  If it finds one, instantiates
          the corresponding request handler and calls it with
          the request method and the match groups.
          
          If calling the handler errors (which is shouldn't normally
          do -- the handler should catch the error), returns a 
          minimalist 500 response.
          
          If no match is found, returns a minimalist 404 response.
          
        """
        
        request = self._Request(environ)
        response = self._Response(status=200, content_type=self._content_type)
        
        handler_class, groups = self._path_router.match(request.path)
        if handler_class is not None:
            handler = handler_class(request, response)
            try:
                response = handler(environ['REQUEST_METHOD'], *groups)
            except Exception, err: # handler should catch all exceptions
                response.status = 500
        else: # to handle 404 nicely, define a catch all url handler
            response.status = 404
        
        return response(environ, start_response)
        
    
    

