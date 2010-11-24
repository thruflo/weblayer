#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `WSGIApplication`_ and `RequestHandler` implementations.
  
  .. _`WSGIApplication`: http://pythonpaste.org/
"""

import datetime

from zope.component import adapts
from zope.interface import implements

from interfaces import IWSGIApplication, IRequestHandler
from interfaces import IRequest, IResponse, ITemplateRenderer

class FooWSGIApplication(object):
    """
    """
    
    implements(IWSGIApplication)
    

class BarRequestHandler(object):
    """
    """
    
    adapts(IRequest, IResponse, ITemplateRenderer)
    implements(IRequestHandler)
    





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


