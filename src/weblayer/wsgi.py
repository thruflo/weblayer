#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" :py:mod:`weblayer.wsgi` provides :py:class:`WSGIApplication`, an
  implementation of :py:class:`~weblayer.interfaces.IWSGIApplication` that
  adapts :py:class:`~weblayer.interfaces.ISettings` and an 
  :py:class:`~weblayer.interfaces.IPathRouter`::
  
      >>> settings = {}
      >>> path_router = object()
  
  To provide a callable `WSGI`_ application::
  
      >>> application = WSGIApplication(settings, path_router)
  
  .. _`WSGI`: http://www.python.org/dev/peps/pep-0333/
"""

__all__ = [
    'WSGIApplication'
]

from zope.component import adapts
from zope.interface import implements

from base import Request, Response
from interfaces import IPathRouter, ISettings, IWSGIApplication

class WSGIApplication(object):
    
    adapts(ISettings, IPathRouter)
    implements(IWSGIApplication)
    
    def __init__(
            self,
            settings,
            path_router,
            request_class=None,
            response_class=None,
            default_content_type='text/html; charset=UTF-8'
        ):
        """
        """
        
        self._settings = settings
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
        """ Checks ``self._path_router`` for a 
          :py:meth:`~weblayer.interfaces.IPathRouter.match` against the
          incoming :py:attr:`~weblayer.interfaces.IRequest.path`::
          
              handler_class, args, kwargs = self._path_router.match(request.path)
          
          If ``handler_class`` is not ``None``, instantiates the
          :py:class:`~weblayer.interfaces.IRequestHandler`::
          
              handler = handler_class(request, response, self._settings)
          
          And calls it with ``environ['REQUEST_METHOD']`` and the ``args`` and 
          ``kwargs`` from :py:meth:`~weblayer.interfaces.IPathRouter.match`::
          
              response = handler(environ['REQUEST_METHOD'], *args, **kwargs)
          
          .. note::
          
              If calling the handler errors (which is shouldn't normally do, as
              the handler *should* catch the error), returns a minimalist 500 
              response.
          
          .. note::
          
              If no match is found, returns a minimalist 404 response.  To handle
              404 responses more elegantly, define a catch all URL handler.
          
        """
        
        request = self._Request(environ)
        response = self._Response(
            request=request, 
            status=200, 
            content_type=self._content_type
        )
        
        handler_class, args, kwargs = self._path_router.match(request.path)
        if handler_class is not None:
            handler = handler_class(request, response, self._settings)
            try: # handler *should* catch all exceptions
                response = handler(environ['REQUEST_METHOD'], *args, **kwargs)
            except Exception: # unless deliberately bubbling them up
                if environ.get('paste.throw_errors', False): 
                    raise
                else:
                    response.status = 500
        else: # to handle 404 nicely, define a catch all url handler
            response.status = 404
        
        return response(environ, start_response)
        
    
    

