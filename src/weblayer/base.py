#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" :py:mod:`weblayer.base` provides default 
  :py:class:`~weblayer.interfaces.IRequest` and 
  :py:class:`~weblayer.interfaces.IResponse` implementations, based purely on
  `webob.Request`_ and `webob.Response`_.
  
  The two implementations, :py:class:`Request` and :py:class:`Response`, add
  no functionality to their `WebOb`_ superclasses beyond declaring that they
  implement the :py:class:`~weblayer.interfaces.IRequest` and 
  :py:class:`~weblayer.interfaces.IResponse` interfaces.
  
  .. _`webob.Request`: http://pythonpaste.org/webob/reference.html#id1
  .. _`webob.Response`: http://pythonpaste.org/webob/reference.html#id2
"""

__all__ = [
    'Request',
    'Response'
]

import webob

from zope.interface import implements

from interfaces import IRequest, IResponse

class Request(webob.Request):
    """ :py:class:`~weblayer.interfaces.IRequest` implementation using 
      `webob.Request`_.
      
      .. _`webob.request`: http://pythonpaste.org/webob/reference.html#id1
    """
    
    implements(IRequest)
    

class Response(webob.Response):
    """ :py:class:`~weblayer.interfaces.IResponse` implementation using 
      `webob.Response`_.
      
      .. _`webob.response`: http://pythonpaste.org/webob/reference.html#id2
    """
    
    implements(IResponse)
    


Request.ResponseClass = Response
Response.RequestClass = Request
