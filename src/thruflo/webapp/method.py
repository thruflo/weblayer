#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Method exposing.
"""

__all__ = [
    'ExposedMethodSelector'
]

from functools import wraps

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequestHandler, IMethodSelector

def expose(method):
    """ Decorator to expose a request handler method.
    """
    
    @wraps(method)
    def _expose(self):
        """ Ensures `method.__name__` is in `self.__exposed_methods__`.
        """
        
        if not IRequestHandler.implementedBy(self):
            error_msg = u'`{}` must implement `{}`'.format(
                self,
                IRequestHandler
            )
            raise TypeError(error_msg)
        
        if not hasattr(self, '__exposed_methods__'):
            self.__exposed_methods__ = []
        
        if not method.__name__ in self.__exposed_methods__:
            self.__exposed_methods__.append(method.__name__)
        
    
    return _expose
    


class ExposedMethodSelector(object):
    """ Method selector adapter that works in tandem with 
      the `expose` decorator.
    """
    
    adapts(IRequestHandler)
    implements(IMethodSelector)
    
    def __init__(self, context):
        self.context = context
        
    
    
    def select_method(self, method_name):
        """ Returns `getattr(self, method_name)` iff the method exists
          and is exposed.  Otherwise returns `None`.
        """
        
        if not isinstance(method_name, basestring):
            raise ValueError
        
        method_name = method_name.lower()
        if method_name in self.context.__exposed_methods__:
            return getattr(self.context, method_name, None)
        
        
    
    

