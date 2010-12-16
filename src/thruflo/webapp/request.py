#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `IRequestHandler` implementation.
"""

__all__ = [
    'RequestHandler'
]

from os.path import dirname, join as join_path

from zope.component import adapts
from zope.interface import implements

from component import registry

from interfaces import IRequest, IResponse, IRequestHandler
from settings import require
from utils import generate_hash, xhtml_escape

class XSRFError(ValueError):
    """ Raised when xsrf validation fails.
    """
    


@require('static_path')
@require('static_url_prefix', default=u'/static/')
@require('check_xsrf', default=True)
class RequestHandler(object):
    """
    """
    
    adapts(IRequest, IResponse)
    implements(IRequestHandler)
    
    def __init__(
            self, 
            request,
            response,
            settings=None,
            template_renderer=None,
            authentication_manager_adapter=None,
            secure_cookie_wrapper_adapter=None,
            method_selector_adapter=None,
            response_normaliser_adapter=None
        ):
        """
        """
        
        self.request = request
        self.response = response
        
        if settings is None:
            settings = registry.lookup('settings')
        if template_renderer is None:
            template_renderer = registry.lookup('template_renderer')
            
        if authentication_manager_adapter is None:
            authentication_manager_adapter = registry.lookup(
                'authentication_manager', 
                'request_handler'
            )
        self.auth = authentication_manager_adapter(self)
        
        if secure_cookie_wrapper_adapter is None:
            secure_cookie_wrapper_adapter = registry.lookup(
                'secure_cookie_wrapper', 
                'request_handler'
            )
        self.cookies = secure_cookie_wrapper_adapter(self)
        
        if method_selector_adapter is None:
            method_selector_adapter = registry.lookup(
                'method_selector', 
                'request_handler'
            )
        self._method_selector = method_selector_adapter(self)
        
        if response_normaliser_adapter is None:
            self._ResponseNormaliser = registry.lookup(
                'response_normaliser', 
                'response'
            )
        else:
            self._ResponseNormaliser = response_normaliser_adapter
        
    
    
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
        
    
    def get_xsrf_token(self):
        """ The XSRF-prevention token for the current user/session.
        """
        
        if not hasattr(self, '_xsrf_token'):
            token = self.cookies.get('_xsrf')
            if not token:
                token = generate_hash()
                self.cookies.set('_xsrf', token, expires_days=None)
            self._xsrf_token = token
        return self._xsrf_token
        
    
    def get_xsrf_form_html(self):
        """ An HTML <input/> element to be included with 
          all POST forms.
        """
        
        if not hasattr(self, '_xsrf_form_html'):
            v = self._xhtml_escape(self.get_xsrf_token())
            tag = u'<input type="hidden" name="_xsrf" value="{}"/>'
            self._xsrf_form_html = tag.format(v)
        return self._xsrf_form_html
        
    
    def validate_xsrf(self):
        """ Raise an `XSRFError` if the '_xsrf' argument isn't present
          or if it doesn't match the '_xsrf'.
        """
        
        if self.context.request.method != "POST":
            return
        
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return
            
        request_token = self.context.get_argument('_xsrf', None)
        if request_token is None:
            raise XSRFError(u'`_xsrf` argument missing from POST')
            
        if self.get_xsrf_token() != request_token:
            raise XSRFError(u'XSRF cookie does not match POST argument')
            
        
    
    
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
        
        response_normaliser = self._ResponseNormaliser(self.response)
        return response_normaliser.normalise(handler_response)
        
    
    

