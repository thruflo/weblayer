#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Use the `@expose` decorator to expose request handler methods::
  
      >>> @expose('get')
      ... class MockHandler(object):
      ...     implements(IRequestHandler)
      ...     
      ...     def get(self):
      ...         pass
      ...     
      ...     def post(self):
      ...         pass
      ...     
      ... 
      >>> handler = MockHandler()
  
  This then works in tandem with the `ExposedMethodSelector`
  implementation of `IMethodSelector`::
  
      >>> selector = ExposedMethodSelector(handler)
      >>> selector.select_method('POST') # returns None
      >>> selector.select_method('_do_something_bad') # returns None
      >>> selector.select_method('GET') == handler.get
      True
  
"""

__all__ = [
    'expose',
    'ExposedMethodSelector'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequestHandler, IMethodSelector

class expose(object):
    """ Decorator to expose a request handler's methods.
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
        
        
    
    

