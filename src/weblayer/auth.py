#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A trivial authentication manager.
"""

__all__ = [
    'TrivialAuthenticationManager'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequest, IAuthenticationManager

class TrivialAuthenticationManager(object):
    """ Uses `self.request.remote_user` .
    """
    
    adapts(IRequest)
    implements(IAuthenticationManager)
    
    def __init__(self, request):
        self.request = request
        
    
    
    @property
    def is_authenticated(self):
        """ Is there a `remote_user` in the request?
          
              >>> from mock import Mock
              >>> request = Mock()
          
          If `remote_user` is None, returns `False`::
          
              >>> request.remote_user = None
              >>> am = TrivialAuthenticationManager(request)
              >>> am.is_authenticated
              False
          
          Otherwise returns `True`::
          
              >>> request.remote_user = 'foo'
              >>> am = TrivialAuthenticationManager(request)
              >>> am.is_authenticated
              True
          
        """
        
        return self.request.remote_user is not None
        
    
    
    @property
    def current_user(self):
        """ Returns `request.remote_user`::
          
              >>> from mock import Mock
              >>> request = Mock()
              >>> request.remote_user = 'joe'
              >>> am = TrivialAuthenticationManager(request)
              >>> am.current_user
              'joe'
          
        """
        
        return self.request.remote_user
        
    
    

