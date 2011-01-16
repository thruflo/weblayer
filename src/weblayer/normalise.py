#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" :py:mod:`weblayer.normalise` provides 
  :py:class:`DefaultToJSONResponseNormaliser`, an implementation of
  :py:class:`~weblayer.interfaces.IResponseNormaliser`.
  
  :py:class:`DefaultToJSONResponseNormaliser` adapts a response object::
  
      >>> from mock import Mock
      >>> response = Mock()
      >>> normaliser = DefaultToJSONResponseNormaliser(response)
      >>> normaliser.response == response
      True
  
  Provides a ``normalise()`` method that takes a single argument and uses it to
  update and or replace the original response object before returning it::
  
      >>> class MockResponse(object):
      ...     implements(IResponse)
      ... 
      >>> mock_response = MockResponse()
      >>> r = normaliser.normalise(mock_response)
      >>> r == mock_response
      True
      >>> r = normaliser.normalise('a')
      >>> r.body == 'a'
      True
      >>> r = normaliser.normalise(u'a')
      >>> r.unicode_body == u'a'
      True
  
  This implementation's default behaviour for stuff it can't identify as an
  :py:class:`~weblayer.interfaces.IResponse` or ``basestring`` is to try to
  `JSON`_ encode it::
  
      >>> r = normaliser.normalise({'a': u'b'})
      >>> r.content_type
      'application/json; charset=UTF-8'
      >>> r.unicode_body
      u'{"a": "b"}'
  
  When used to normalise the return value of a request handler method, this
  lets the request handler method return a string or JSON encodable object, 
  without having to worry about constructing a response object, whilst still
  allowing for a response object to be returned when necessary.
  
  .. _`json`: http://www.json.org/
"""

__all__ = [
    'DefaultToJSONResponseNormaliser'
]

from zope.component import adapts
from zope.interface import implements

from interfaces import IResponse, IResponseNormaliser
from utils import json_encode as utils_json_encode

class DefaultToJSONResponseNormaliser(object):
    """ Adapter to normalise a response.
    """
    
    adapts(IResponse)
    implements(IResponseNormaliser)
    
    def __init__(
            self, 
            response, 
            json_encode=None,
            json_content_type='application/json; charset=UTF-8'
        ):
        """ Initialise a `DefaultToJSONResponseNormaliser`::
          
              >>> response = object()
              >>> json_content_type = 'a'
              >>> json_encode = object()
              >>> normaliser = DefaultToJSONResponseNormaliser(
              ...     response,
              ...     json_content_type=json_content_type,
              ...     json_encode=json_encode
              ... )
          
          ``response`` is available as ``self.response``::
          
              >>> normaliser.response == response
              True
              
          ``json_encode`` is available as ``self._json_encode``::
          
              >>> normaliser._json_encode == json_encode
              True
          
          ``json_content_type`` is available as ``self._json_content_type``::
              
              >>> normaliser._json_content_type == json_content_type
              True
              
          which defaults to ``'application/json; charset=UTF-8'``::
          
              >>> default = 'application/json; charset=UTF-8'
              >>> normaliser = DefaultToJSONResponseNormaliser(
              ...     response,
              ...     json_encode=json_encode
              ... )
              >>> normaliser._json_content_type == default
              True
          
        """
        
        self.response = response
        if json_encode is None:
            self._json_encode = utils_json_encode
        else:
            self._json_encode = json_encode
        self._json_content_type = json_content_type
        
    
    def normalise(self, handler_response):
        """ Update and return self.response appropriately.
          
          If ``handler_response`` implements 
          :py:class:`~weblayer.interfaces.IResponse` then just use that::
          
              >>> from mock import Mock
              >>> response = Mock()
              >>> normaliser = DefaultToJSONResponseNormaliser(
              ...     response,
              ...     json_encode=None
              ... )
              >>> class MockResponse(object):
              ...     implements(IResponse)
              ... 
              >>> mock_response = MockResponse()
              >>> r = normaliser.normalise(mock_response)
              >>> r == mock_response
              True
          
          Otherwise if it's a ``str`` or a ``unicode`` use that as the
          response body::
          
              >>> r = normaliser.normalise('a')
              >>> r.body == 'a'
              True
              >>> r = normaliser.normalise(u'a')
              >>> r.unicode_body == u'a'
              True
          
          If it's ``None`` then just return the origin ``response``::
          
              >>> normaliser = DefaultToJSONResponseNormaliser(
              ...     42,
              ...     json_encode=None
              ... )
              >>> normaliser.normalise(None)
              42
          
          Otherwise (with this particular implementation) assume we want to
          encode ``handler_response`` as a JSON string as use that as the
          response body::
          
              >>> response = Mock()
              >>> json_encode = Mock()
              >>> normaliser = DefaultToJSONResponseNormaliser(
              ...     response,
              ...     json_encode=json_encode
              ... )
              >>> json_encode.return_value = '{"a": "b"}'
              >>> r = normaliser.normalise({'a': 'b'})
              >>> r.content_type == normaliser._json_content_type
              True
              >>> json_encode.call_args[0][0] == {'a': 'b'}
              True
              >>> r.body
              '{"a": "b"}'
              >>> json_encode.return_value = u'{"a": "b"}'
              >>> r = normaliser.normalise({'a': u'b'})
              >>> r.unicode_body
              u'{"a": "b"}'
          
        """
        
        if IResponse.providedBy(handler_response):
            self.response = handler_response
        elif isinstance(handler_response, str):
            self.response.body = handler_response
        elif isinstance(handler_response, unicode):
            self.response.unicode_body = handler_response
        elif handler_response is None: # leave self.response alone
            pass
        else: # assume it's json data
            self.response.content_type = self._json_content_type
            json_string = self._json_encode(handler_response)
            if isinstance(json_string, str):
                self.response.body = json_string
            else: # isinstance(json_string, unicode):
                self.response.unicode_body = json_string
        return self.response
        
    
    

