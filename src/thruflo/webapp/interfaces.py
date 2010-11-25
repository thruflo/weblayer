#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `Interface`_ definitions.
  
  .. _`Interface`: http://pypi.python.org/pypi/zope.interface
"""

__all__ = [
    'IWSGIApplication',
    'IRequestHandler',
    'IRequest',
    'IResponse',
    'ITemplateRenderer',
    'IURLMapping'
]

from zope.interface import Interface, Attribute

class IWSGIApplication(Interface):
    """ Callable WSGI application.
    """
    
    def __call__(environ, start_response):
        """ Handle a new request.
        """
        
    
    

class IRequestHandler(Interface):
    """ Takes a request and returns a response.
    """
    
    def set_secure_cookie(name, value, expires_days=30, **kwargs):
        """ Signs and timestamps a cookie so it cannot be forged.
        """
        
    
    def get_secure_cookie(name, include_name=True, value=None):
        """ Returns the given signed cookie if it validates, or None.
        """
        
    
    
    xsrf_token = Attribute(u'XSRF-prevention token.')
    def check_xsrf_cookie():
        """ Verifies that the '_xsrf' cookie matches the '_xsrf' argument.
        """
        
    
    def xsrf_form_html(self):
        """An HTML <input/> element to be included with all POST forms.
        """
        
    
    
    def static_url(self, path):
        """Returns a static URL for the given relative static file path.
        """
        
    
    
    def render_template(self, tmpl_name, **kwargs):
        """ Render template.
        """
        
    
    def redirect(self, url, status=302, content_type=None):
        """ Redirect.
        """
        
    
    def error(self, status=500, body=u'System Error'):
        """ Clear response and return error.
        """
        
    
    def _handle_system_error(self, err):
        """ Override to handle errors nicely.
        """
        
    
    def _handle_method_not_found(self, method_name):
        """ Override to handle 405 nicely.
        """
        
    
    
    def __call__(method_name, *groups):
        """ Call the appropriate method to return a response.
        """
        
    
    

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
        
    
    

class IURLMapping(Interface):
    """ Maps urls to request handlers.
    """
    
    mapping = Attribute(u'List of (compiled_regexp, request_handler) tuples')
    

class IMethodSelector(Interface):
    """ Selects methods by name.
    """
    
    def select_method(method_name):
        """ Return a method using `method_name`.
        """
        
    
    

