#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Use the `@expose` decorator to expose request handler methods::
  
      >>> class MockHandler(object):
      ...     implements(IRequestHandler)
      ...     
      ...     @expose
      ...     def get(self):
      ...         pass
      ...     
      ... 
  
  Then, once we've executed a `venusian` scan (which we fake here
  see `./tests/test_method.py` for an integration test)::
  
      >>> _expose('get', MockHandler)
  
  This works in tandem with the `ExposedMethodSelector`::
  
      >>> handler = MockHandler()
      >>> selector = ExposedMethodSelector(handler)
      >>> selector.select_method('POST') # returns None
      >>> selector.select_method('_do_something_bad') # returns None
      >>> selector.select_method('GET') #doctest: +ELLIPSIS
      <bound method MockHandler.get ...>
  
  To (only) allow `MockHandler` to only accept 'GET' requests.
  
"""

__all__ = [
    'expose',
    'ExposedMethodSelector'
]

import venusian

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequestHandler, IMethodSelector

def _expose(method_name, class_):
    """ Ensures `method_name` is in `class_.__exposed_methods__` 
      iff `class_` implements `IRequestHandler`.
      
          >>> from mock import Mock
          >>> class Handler(Mock):
          ...     implements(IRequestHandler)
          ... 
      
      Method names are in `class_.__exposed_methods__`::
      
          >>> _expose('a', Handler)
          >>> Handler.__exposed_methods__
          ['a']
      
      Method name only appears once, no matter how many
      times it's exposed::
          
          >>> _expose('a', Handler)
          >>> _expose('b', Handler)
          >>> _expose('b', Handler)
          >>> Handler.__exposed_methods__
          ['a', 'b']
      
      Iff `class_` implements `IRequestHandler`::
          
          >>> _expose('b', Mock) #doctest: +ELLIPSIS
          Traceback (most recent call last):
          ...
          TypeError: `<class ... must implement ....IRequestHandler>`
      
    """
    
    if not IRequestHandler.implementedBy(class_):
        error_msg = u'`{}` must implement `{}`'.format(
            class_,
            IRequestHandler
        )
        raise TypeError(error_msg)
    
    if not hasattr(class_, '__exposed_methods__'):
        class_.__exposed_methods__ = []
    
    if not method_name in class_.__exposed_methods__:
        class_.__exposed_methods__.append(method_name)
    

def expose(method, venusian=venusian):
    """ Decorator to expose a request handler's methods.
    """
    
    def callback(scanner, name, ob):
        return _expose(method.__name__, ob)
        
    
    
    venusian.attach(method, callback, category='thruflo')
    return method
    


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
        
        
    
    

