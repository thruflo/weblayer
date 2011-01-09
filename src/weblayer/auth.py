#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" :py:mod:`weblayer.auth` provides :py:class:`TrivialAuthenticationManager`,
  an implementation of :py:class:`~weblayer.interfaces.IAuthenticationManager`.
  
  The implementation is deliberately trivial as it's envisaged that a bespoke 
  application that requires authentication will:
  
  * use WSGI middleware (for example `AuthKit`_ or `repoze.who`_) to handle
    authentication; and / or
  * override the :py:class:`~weblayer.interfaces.IAuthenticationManager`
    implementation to work with the individual application's persistence and
    caching layers.
  
  .. _`AuthKit`: http://authkit.org/
  .. _`repoze.who`: http://docs.repoze.org/who
"""

__all__ = [
    'TrivialAuthenticationManager'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequest, IAuthenticationManager

class TrivialAuthenticationManager(object):
    """ A very simple :py:class:`~weblayer.interfaces.IAuthenticationManager`
      implementation that uses the `webob.Request`_ attribute 
      :py:obj:`request.remote_user` which, under the `WebOb`_ hood, is derived
      from :py:obj:`request.environ['REMOTE_USER']`, which is 
      `the standard place`_ for authentication middleware to put a user id.
      
      :py:class:`TrivialAuthenticationManager` is thus perfectly usable in
      many cases with :py:attr:`is_authenticated` returning `True` or `False`
      appropriately and :py:attr:`current_user` returning a user id if present
      or `None` if not.
      
      .. _`webob`: http://pythonpaste.org/webob
      .. _`webob.request`: http://pythonpaste.org/webob/reference.html#id1
      .. _`the standard place`: http://wsgi.org/wsgi/Specifications/simple_authentication
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
        
    
    

