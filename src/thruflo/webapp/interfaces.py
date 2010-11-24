#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `Interface`_ definitions.
  
  .. _`Interface`: http://pypi.python.org/pypi/zope.interface
"""

__all__ [
    'IWSGIApplication',
    'IRequestHandler',
    'IRequest',
    'IResponse',
    'ITemplateRenderer'
]

from zope.interface import Interface, Attribute

class IWSGIApplication(Interface):
    """ Callable WSGI application that responds to requests.
    """
    
    def __call__(environ, start_response):
        """ Handle a new request.
        """
        
    
    

class IRequestHandler(Interface):
    """
    """
    
    cookies = Attribute(u'A dictionary of Cookie.Morsel objects.')
    def get_cookie(name, default=None):
        """ Gets the value of the cookie with the given name.
        """
        
    
    def set_cookie(
            name, 
            value, 
            domain=None, 
            expires=None, 
            path="/", 
            expires_days=None, 
            override=False
        ):
        """ Sets the given cookie name/value with the given options.
        """
        
    
    def set_secure_cookie(name, value, expires_days=30, **kwargs):
        """ Signs and timestamps a cookie so it cannot be forged.
        """
        
    
    def get_secure_cookie(name, include_name=True, value=None):
        """ Returns the given signed cookie if it validates, or None.
        """
        
    
    def delete_cookie(name, path="/", domain=None):
        """ Deletes the cookie with the given name.
        """
        
    
    
    # @@ ...
    

class IRequest(Interface):
    """ An HTTP Request object.
    """
    
    url = Attribute(u'Full request URL, including QUERY_STRING')
    host = Attribute(u'HOST provided in HTTP_HOST w. fall-back to SERVER_NAME')
    host_url = Attribute(u'The URL through the HOST (no path)')
    application_url = Attribute(u'URL w. SCRIPT_NAME no PATH_INFO or QUERY_STRING')
    path_url = Attribute(u'URL w. SCRIPT_NAME & PATH_INFO no QUERY_STRING')
    path = Attribute(u'Path of the request, without HOST or QUERY_STRING')
    path_qs = Attribute(u'Path without HOST but with QUERY_STRING')
    
    headers = Attribute(u'Headers as case-insensitive dictionary-like object')
    params = Attribute(u'Dictionary-like obj of params from POST and QUERY_STRING')
    body = Attribute(u'Content of the request body.')
    
    cookies = Attribute(u'Dictionary of cookies found in the request')
    

class IResponse(Interface):
    """ An HTTP Response object.
    """
    
    headers = Attribute(u'The headers in a dictionary-like object')
    headerlist = Attribute(u'The list of response headers')
    
    body = Attribute(u'The body of the response, as a ``str``.')
    unicode_body = Attribute(u'The body of the response, as a ``unicode``.')
    
    content_type = Attribute(u'The `Content-Type` header')
    status = Attribute(u'The `status` string')
    
    def set_cookie(key, value='', **kwargs):
        """ Set (add) a cookie for the response.
        """
        
    
    def unset_cookie(key, strict=True):
        """ Unset a cookie with the given name.
        """
        
    
    def delete_cookie(key, **kwargs):
        """ Delete a cookie from the client.
        """
        
    
    

class ITemplateRenderer(Interface):
    """ A utility which renders templates.
    """
    
    def render(tmpl_name, **kwargs):
        """ Render a template identified with `tmpl_name`.
        """
        
    
    

