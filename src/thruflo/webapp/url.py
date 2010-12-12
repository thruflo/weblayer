#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A simple URL mapping implementation.
"""

__all__ = [
    'SimpleURLMapping'
]

import re

from zope.interface import implements

from interfaces import IURLMapping, IRequestHandler

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
    



class SimpleURLMapping(object):
    """ Provides a `mapping` of compiled regular expressions 
      to request handlers.
    """
    
    implements(IURLMapping)
    
    mapping = []
    
    def __init__(self, raw_mapping, compile=_compile_top_and_tailed):
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
              >>> um = SimpleURLMapping(raw_mapping, compile=mock_compile)
              >>> isinstance(um.mapping, list)
              True
              >>> isinstance(um.mapping[0], tuple)
              True
              >>> um.mapping[0][1] == MockHandler
              True
          
          As long as `raw_mapping` can be unpacked into pairs of items::
          
              >>> raw_mapping = [('a')]
              >>> SimpleURLMapping(raw_mapping) #doctest: +ELLIPSIS
              Traceback (most recent call last):
              ...
              ValueError: need more than 1 value to unpack
          
          The first item of each pair is passed to `compile`::
          
              >>> mock_compile.call_args[0][0] == r'/foo'
              True
              >>> um.mapping[0][0] == mock_compile.return_value
              True
          
          Iff the second item implements `IRequestHandler`::
          
              >>> SimpleURLMapping([(r'/foo', Mock)]) #doctest: +ELLIPSIS
              Traceback (most recent call last):
              ...
              TypeError: `<class ... must implement ....IRequestHandler>`
          
        """
        
        for regexp, handler_class in raw_mapping:
            if not IRequestHandler.implementedBy(handler_class):
                error_msg = u'`{}` must implement `{}`'.format(
                    handler_class, 
                    IRequestHandler
                )
                raise TypeError(error_msg)
            self.mapping.append((compile(regexp), handler_class))
        
    
    

