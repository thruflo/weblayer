#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" IPathRouter implementation that uses regexp patterns.
  
  Say, for example, you have some request handlers::
  
      >>> class DummyIndex(object):
      ...     implements(IRequestHandler)
      ... 
      >>> class Dummy404(object):
      ...     implements(IRequestHandler)
      ... 
  
  You can then map request paths to them using a simple list 
  of two item tuples::
  
      >>> mapping = [(
      ...         # string or compiled regexp pattern to match
      ...         # against the request path
      ...         r'/',
      ...         # class the request should be handled by
      ...         DummyIndex
      ...     ), (
      ...         r'(.*)',
      ...         Dummy404
      ...     )
      ... ]
      >>> path_router = RegExpPathRouter(mapping)
  
  And use the path router to get handlers for request paths::
  
      >>> path_router.match('/') == (DummyIndex, ())
      True
  
  Returning the handler and the match groups if any::
  
      >>> path_router.match('/foobar') == (Dummy404, ('/foobar',))
      True
  
  The mapping items are looked up in order::
  
      >>> mapping.reverse()
      >>> path_router = RegExpPathRouter(mapping)
      >>> path_router.match('/') == (Dummy404, ('/',))
      True
  
  If the path doesn't match, returns `(None, None)`::
  
      >>> path_router = RegExpPathRouter([])
      >>> path_router.match('/')
      (None, None)
  
"""

__all__ = [
    'RegExpPathRouter'
]

import re

from zope.interface import implements

from interfaces import IPathRouter, IRequestHandler

_RE_TYPE = type(re.compile(r''))
def _compile_top_and_tailed(string_or_compiled_pattern):
    """ If `string_or_compiled_pattern` is a compiled pattern,
      just return it::
      
          >>> p = r'^foobar$'
          >>> c = re.compile(p)
          >>> _compile_top_and_tailed(c) == c
          True
          
      Otherwise if it's a `basestring` compile and return it::
      
          >>> _compile_top_and_tailed(p) == c
          True
          >>> _compile_top_and_tailed({})
          Traceback (most recent call last):
          ...
          TypeError: `{}` must be string or compiled pattern
      
      Prepending '^' if `pattern` doesn't already start with it::
      
          >>> p2 = r'foobar$'
          >>> _compile_top_and_tailed(p2) == c
          True
      
      Appending '$' if it doesn't already start with it::
      
          >>> p3 = r'^foobar'
          >>> _compile_top_and_tailed(p3) == c
          True
      
    """
    
    if isinstance(string_or_compiled_pattern, _RE_TYPE):
        return string_or_compiled_pattern
    
    s = string_or_compiled_pattern
    if not isinstance(s, basestring):
        error_msg = u'`{}` must be string or compiled pattern'.format(s)
        raise TypeError(error_msg)
    
    if not s.startswith('^'):
        s = r'^{}'.format(s)
    if not s.endswith('$'):
        s = r'{}$'.format(s)
    
    return re.compile(s)
    


class RegExpPathRouter(object):
    """ Routes paths to request handlers using regexp patterns.
    """
    
    implements(IPathRouter)
    
    def __init__(self, raw_mapping, compile_=None):
        """ Takes a list of raw regular expressions mapped to request 
          handler classes, compiles the regular expressions and 
          provides `.mapping`.
          
              >>> from mock import Mock
              >>> mock_compile = Mock()
              >>> mock_compile.return_value = re.compile(r'^/foo$')
              >>> class MockHandler(object):
              ...     implements(IRequestHandler)
              ... 
              >>> raw_mapping = [(
              ...         r'/foo',
              ...         MockHandler
              ...     )
              ... ]
              >>> path_router = RegExpPathRouter(raw_mapping, compile_=mock_compile)
              >>> isinstance(path_router._mapping, list)
              True
              >>> isinstance(path_router._mapping[0], tuple)
              True
              >>> path_router._mapping[0][1] == MockHandler
              True
          
          The first item of each pair is passed to `compile`::
          
              >>> mock_compile.call_args[0][0] == r'/foo'
              True
              >>> path_router._mapping[0][0] == mock_compile.return_value
              True
          
          As long as `raw_mapping` can be unpacked into pairs of items::
          
              >>> raw_mapping = [('a')]
              >>> RegExpPathRouter(raw_mapping) #doctest: +ELLIPSIS
              Traceback (most recent call last):
              ...
              ValueError: need more than 1 value to unpack
          
          And the second item implements `IRequestHandler`::
          
              >>> RegExpPathRouter([(r'/foo', Mock)]) #doctest: +ELLIPSIS
              Traceback (most recent call last):
              ...
              TypeError: `<class ... must implement ....IRequestHandler>`
          
        """
        
        compile_ = compile_ is None and _compile_top_and_tailed or compile_
        
        self._mapping = []
        
        for regexp, handler_class in raw_mapping:
            if not IRequestHandler.implementedBy(handler_class):
                error_msg = u'`{}` must implement `{}`'.format(
                    handler_class, 
                    IRequestHandler
                )
                raise TypeError(error_msg)
            
            self._mapping.append((compile_(regexp), handler_class))
            
        
    
    def match(self, path):
        """ Iterate through self._mapping.  If the path matches an item, 
          return the handler class and the `re` `match` object's groups, 
          otherwise return `(None, None)`.
        """
        
        for regexp, handler_class in self._mapping:
            match = regexp.match(path)
            if match:
                return handler_class, match.groups()
        
        return None, None
        
    
    

