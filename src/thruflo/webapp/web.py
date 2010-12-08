#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `WSGIApplication`_ and `RequestHandler` implementations.
  
  .. _`WSGIApplication`: http://pythonpaste.org/
"""

__all__ = [
    'Request',
    'Response',
    'RequestHandler',
    'WSGIApplication'
]


import binascii
import logging
import uuid

from os.path import dirname, join as join_path

import webob

from zope.component import adapts
from zope.interface import implements

from interfaces import *
from utils import generate_hash
from settings import require_setting

require_setting('check_xsrf', default=True)
require_setting('static_path')
require_setting('static_url_prefix', default=u'/static/')

class Request(webob.Request):
    """ We use `webob.Request` as our default
      `IRequest` implementation.
    """
    
    implements(IRequest)
    

class Response(webob.Response):
    """ We use `webob.Response` as our default
      `IResponse` implementation.
    """
    
    implements(IResponse)
    

class RequestHandler(object):
    """
    """
    
    adapts(IRequest, IResponse, IApplicationSettings, ITemplateRenderer)
    implements(IRequestHandler)
    
    def __init__(self, request, response, settings, template_renderer):
        """
        """
        
        self.request = request
        self.response = response
        self.settings = settings
        self.template_renderer = template_renderer
        
        self.auth = IAuthenticationManager(self)
        self.cookies = ICookieWrapper(self)
        self.xsrf = IXSRFValidator(self)
        
        self._method_selector = IMethodSelector(self)
        
    
    
    def get_static_url(self, path):
        """ Returns a static URL for the given relative 
          static file path.
        """
        
        if not hasattr(RequestHandler, "_static_hashes"):
            RequestHandler._static_hashes = {}
        
        hashes = RequestHandler._static_hashes
        if path not in hashes:
            file_path = join_path(self.settings["static_path"], path)
            try:
                f = open(file_path)
            except IOError:
                logging.error("Could not open static file %r", path)
                hashes[path] = None
            else:
                hashes[path] = generate_hash(s=f.read())
                f.close()
        base = self.request.host_url
        static_url_prefix = self.settings['static_url_prefix']
        if hashes.get(path):
            return base + static_url_prefix + path + "?v=" + hashes[path][:5]
        else:
            return base + static_url_prefix + path
        
    
    
    def get_argument(self, name, default=None, strip=False):
        args = self.get_arguments(name, strip=strip)
        if not args:
            return default
        return args[-1]
        
    
    def get_arguments(self, name, strip=False):
        values = self.request.params.get(name, [])
        if not bool(isinstance(values, list) or isinstance(values, tuple)):
           values = [values]
        if strip:
            values = [x.strip() for x in values]
        return values
        
    
    
    def render(self, tmpl_name, **kwargs):
        """ Render template.
        """
        
        params = dict(
            request=self.request,
            current_user=self.auth.current_user,
            static_url=self.get_static_url,
            xsrf_form_html=self.xsrf.form_html
        )
        params.update(kwargs)
        return self.template_renderer.render(tmpl_name, **params)
        
    
    def redirect(self, url, status=302, content_type=None):
        """ Handle redirecting.
        """
        
        self.response.status = status
        if not self.response.headerlist:
            self.response.headerlist = []
        self.response.headerlist.append(('Location', url))
        if content_type:
            self.response.content_type = content_type
        return self.response
        
    
    def error(self, status=500, body=u'System Error'):
        """ Clear response and return error.
        """
        
        self.response = self.response.__class__(status=status)
        
        if isinstance(body, unicode):
            self.response.unicode_body = body
        else:
            self.response.body = body
        
        return self.response
        
    
    
    def _handle_method_not_found(self, method_name):
        """ Override to handle 405 nicely.
        """
        
        logging.warning(u'{} method not found'.format(method_name))
        return self.error(status=405)
        
    
    def _handle_xsrf_error(self, err):
        """ Override to handle XSRF mismatch nicely.
        """
        
        logging.warning(err)
        return self.error(status=403)
        
    
    def _handle_system_error(self, err):
        """ Override to handle 500 nicely.
        """
        
        logging.error(err, exc_info=True)
        return self.error(status=500)
        
    
    
    def __call__(self, method_name, *groups):
        """
        """
        
        method = self._method_selector.select_method(method_name)
        if method is None:
            handler_response = self._handle_method_not_found(method_name)
        else:
            try:
                if self.settings["check_xsrf"]: self.xsrf.validate_request()
            except XSRFError, err:
                handler_response = self._handle_xsrf_error(err)
            else:
                try:
                    handler_response = method(*groups)
                except Exception, err:
                    handler_response = self._handle_system_error(err)
        
        normaliser = IResponseNormaliser(self.response)
        return normaliser.normalise(handler_response)
        
    
    

class WSGIApplication(object):
    """ Implementation of a callable WSGI application
      that uses a URL mapping to pass requests on.
    """
    
    adapts(IURLMapping, IApplicationSettings, ITemplateRenderer)
    implements(IWSGIApplication)
    
    def __init__(
            self,
            url_mapping,
            settings,
            template_renderer,
            request_class=Request,
            response_class=Response,
            default_content_type='text/html; charset=UTF-8'
        ):
        self._url_mapping = url_mapping
        self._settings = settings
        self._template_renderer = template_renderer
        self._request_class = request_class
        self._response_class = response_class
        self._default_content_type = default_content_type
        
    
    def __call__(self, environ, start_response):
        """ Checks the url mapping for a match against the
          incoming request path.  If it finds one, instantiates
          the corresponding request handler and calls it with
          the request method and the match groups.
          
          If calling the handler errors, returns a minimalist
          500 response.
          
          If no match is found, returns a minimalist 404 response.
          
        """
        
        handler = None
        groups = ()
        
        request = self._request_class(environ)
        response = self._response_class(
            status=200, 
            content_type=self._default_content_type
        )
        
        for regexp, handler_class in self._url_mapping.mapping:
            match = regexp.match(request.path)
            if match:
                handler = handler_class(
                    request, 
                    response, 
                    self._settings,
                    self._template_renderer
                )
                groups = match.groups()
                break
            
        if handler:
            try:
                response = handler(environ['REQUEST_METHOD'], *groups)
            except Exception, err:
                response.status = 500
        else: # to handle 404 nicely, define a catch all url handler
            response.status = 404
        
        return response(environ, start_response)
        
    
    

