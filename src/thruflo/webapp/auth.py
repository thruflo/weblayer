#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Authentication manager.
"""

__all__ = [
    'TrivialAuthenticationManager'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequestHandler, IAuthenticationManager

class TrivialAuthenticationManager(object):
    """ @@ this is just a placeholder...
    """
    
    adapts(IRequestHandler)
    implements(IAuthenticationManager)
    
    def __init__(self, context):
        self.context = context
        
    
    
    @property
    def is_authenticated(self):
        """ @@ ...
        """
        
        return self.context.request.remote_user is not None
        
    
    
    @property
    def current_user(self):
        """ @@ ...
        """
        
        return self.context.request.remote_user
        
    
    

