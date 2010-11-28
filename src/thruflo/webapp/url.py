#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" URL mapping.
"""

__all__ = [
    'SimpleURLMapping'
]

import re

from zope.interface import implements

from interfaces import IURLMapping, IRequestHandler

class SimpleURLMapping(object):
    """ Takes a `list_of_tuples` with two items each, compiles the 
      first value in each tuple to a regular expression, makes 
      sure the second implements `IRequestHandler` and provides 
      the resulting list as `mapping`.
    """
    
    implements(IURLMapping)
    
    mapping = []
    
    def __init__(self, list_of_tuples, sort_order=1):
        """
        """
        
        for regexp, handler_class in list_of_tuples:
            if not IRequestHandler.implementedBy(handler_class):
                error_msg = u'`{}` must implement `{}`'.format(
                    handler_class, 
                    IRequestHandler
                )
                raise TypeError(error_msg)
            self.mapping.append((self._process(regexp), handler_class))
        
    
    
    def _process(self, regexp):
        """ Makes sure the regexp starts with a '^' and ends
          with a '$' and then compiles and returns it.
        """
        
        if not regexp.startswith('^'):
            regexp = r'^{}'.format(regexp)
        if not regexp.endswith('$'):
            regexp = r'{}$'.format(regexp)
        return re.compile(regexp)
        
    
    

