#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Use `RequestHandler.__all__` to explicitly expose public request
  handler methods::
  
      >>> class MockHandler(object):
      ...     implements(IRequestHandler)
      ...     
      ...     __all__ = ('get')
      ...     
      ...     def get(self):
      ...         pass
      ...         
      ...     
      ...     def post(self):
      ...         pass
      ...         
      ...     
      ... 
      >>> handler = MockHandler()
      >>> selector = ExposedMethodSelector(handler)
      >>> callable(selector.select_method('GET'))
      True
      >>> callable(selector.select_method('POST'))
      False
  
"""

__all__ = [
    'ExposedMethodSelector'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequestHandler, IMethodSelector

class ExposedMethodSelector(object):
    """ Method selector adapter that works in tandem with the
      `RequestHandler.__all__` attribute.
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
        
        if not hasattr(self.context, '__all__'):
            return None
        
        method_name = method_name.lower()
        if method_name in self.context.__all__:
            return getattr(self.context, method_name, None)
        
        
    
    

