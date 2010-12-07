#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Method exposing.
"""

__all__ = [
    'ExposedMethodSelector'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequestHandler, IMethodSelector

class expose(object):
    """ Decorator to expose a request handler's methods, e.g.:
      
          @expose('get', 'put', 'delete')
          class MyHandler(...)
              ...
              
          
      
    """
    
    def __init__(self, *method_names):
        self.method_names = method_names
        
    
    
    def __call__(self, class_):
        """ Ensures `self.method_names` are in `class_.__exposed_methods__`
          iff `class_` implements `IRequestHandler`.
        """
        
        if not IRequestHandler.implementedBy(class_):
            error_msg = u'`{}` must implement `{}`'.format(
                class_,
                IRequestHandler
            )
            raise TypeError(error_msg)
        
        if not hasattr(class_, '__exposed_methods__'):
            class_.__exposed_methods__ = []
        
        for method_name in self.method_names:
            if not method_name in class_.__exposed_methods__:
                class_.__exposed_methods__.append(method_name)
            
        return class_
        
    
    


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
        
        if not hasattr(self.context, '__exposed_methods__'):
            return None
        
        method_name = method_name.lower()
        if method_name in self.context.__exposed_methods__:
            return getattr(self.context, method_name, None)
        
        
    
    

