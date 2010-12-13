#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A trivial authentication manager.
"""

__all__ = [
    'TrivialAuthenticationManager'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequestHandler, IAuthenticationManager

class TrivialAuthenticationManager(object):
    """ Uses `self.context.request.remote_user` .
    """
    
    adapts(IRequestHandler)
    implements(IAuthenticationManager)
    
    def __init__(self, context):
        self.context = context
        
    
    
    @property
    def is_authenticated(self):
        """ Is there a `remote_user` in the request?
          
              >>> from mock import Mock
              >>> ctx = Mock()
              >>> ctx.request = Mock()
          
          If `remote_user` is None, returns `False`::
          
              >>> ctx.request.remote_user = None
              >>> am = TrivialAuthenticationManager(ctx)
              >>> am.is_authenticated
              False
          
          Otherwise returns `True`::
          
              >>> ctx.request.remote_user = 'foo'
              >>> am = TrivialAuthenticationManager(ctx)
              >>> am.is_authenticated
              True
          
        """
        
        return self.context.request.remote_user is not None
        
    
    
    @property
    def current_user(self):
        """ Returns `request.remote_user`::
          
              >>> from mock import Mock
              >>> ctx = Mock()
              >>> ctx.request = Mock()
              >>> ctx.request.remote_user = 'joe'
              >>> am = TrivialAuthenticationManager(ctx)
              >>> am.current_user
              'joe'
          
        """
        
        return self.context.request.remote_user
        
    
    

