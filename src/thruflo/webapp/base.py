#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" We base our request handling on `webob.Response`
  and response generation on `webob.Request`.
"""

__all__ = [
    'Request',
    'Response'
]

import webob

from zope.interface import implements

from interfaces import IRequest, IResponse

class Request(webob.Request):
    """ `IRequest` implementation using `webob.Request`.
    """
    
    implements(IRequest)
    

class Response(webob.Response):
    """ `IResponse` implementation using `webob.Response`.
    """
    
    implements(IResponse)
    

