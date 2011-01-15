#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" :py:mod:`weblayer.method` provides :py:class:`ExposedMethodSelector`, an 
  implementation of :py:class:`~weblayer.interfaces.IMethodSelector`.
  
  :py:class:`ExposedMethodSelector` works in tandem with 
  ``RequestHandler.__all__`` to select only explicitly exposed request handler
  methods to handle incoming requests::
  
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
      ``RequestHandler.__all__`` attribute.
    """
    
    adapts(IRequestHandler)
    implements(IMethodSelector)
    
    def __init__(self, context):
        self.context = context
        
    
    def select_method(self, method_name):
        """ Returns ``getattr(self, method_name)`` iff the method exists
          and is exposed.  Otherwise returns ``None``.
          
          Special cases HEAD requests to use GET, iff ``'head'`` is exposed,
          ``def get()`` exists and ``def head()`` doesn't.  This allows
          applications to respond to HEAD requests without writing seperate
          head methods and takes advantage of the special case in 
          ``webob.Response.__call__``::
          
              def __call__(self, environ, start_response):
                  
                  # ... code removed for brevity
                  
                  if environ['REQUEST_METHOD'] == 'HEAD':
                      # Special case here...
                      return EmptyResponse(self.app_iter)
                  return self.app_iter
              
          
        """
        
        if not isinstance(method_name, basestring):
            raise ValueError
        
        if not hasattr(self.context, '__all__'):
            return None
        
        method_name = method_name.lower()
        if method_name in self.context.__all__:
            method = getattr(self.context, method_name, None)
            if method_name == 'head' and method is None: # special case
                if 'get' in self.context.__all__:
                    method = getattr(self.context, 'get', None)
            return method
        
    
    

