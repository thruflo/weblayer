#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `WSGIApplication`_ and `RequestHandler` implementations.
  
  .. _`WSGIApplication`: http://pythonpaste.org/
"""

__all__ = [
    'Request',
    'Response',
    'RequestHandler'
]

import datetime

import webob

from zope.component import adapts, base
from zope.interface import implements

from interfaces import *

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
    
    adapts(IRequest, IResponse)
    implements(IRequestHandler)
    
    def __init__(self, request, response):
        self.request = request
        self.response = response
        self.settings = base.getUtility(ISettings)
        self.template_renderer = base.getUtility(ITemplateRenderer)
        
    
    
    def _cookie_signature(self, *parts):
        h = hmac.new(self.settings["cookie_secret"], digestmod=hashlib.sha1)
        for part in parts: h.update(part)
        return h.hexdigest()
        
    
    def set_secure_cookie(self, name, value, expires_days=30, **kwargs):
        """Signs and timestamps a cookie so it cannot be forged.
          
          You must specify the 'cookie_secret' setting in your Application
          to use this method. It should be a long, random sequence of bytes
          to be used as the HMAC secret for the signature.
          
          To read a cookie set with this method, use get_secure_cookie().
          
        """
        
        timestamp = str(int(time.time()))
        value = base64.b64encode(value)
        signature = self._cookie_signature(name, value, timestamp)
        value = "|".join([value, timestamp, signature])
        max_age = None
        if expires_days:
            max_age = expires_days * 24 * 60 * 60
        self.response.set_cookie(name, value=value, max_age=max_age, **kwargs)
        
    
    def get_secure_cookie(self, name, include_name=True, value=None):
        """Returns the given signed cookie if it validates, or None.
        """
        
        if value is None: 
            value = self.request.cookies.get(name, None)
        
        if not value:
            return None
        
        parts = value.split("|")
        if len(parts) != 3: 
            return None
        
        if include_name:
            signature = self._cookie_signature(name, parts[0], parts[1])
        else:
            signature = self._cookie_signature(parts[0], parts[1])
        
        if not _time_independent_equals(parts[2], signature):
            logging.warning("Invalid cookie signature %r", value)
            return None
        
        timestamp = int(parts[1])
        if timestamp < time.time() - 31 * 86400:
            logging.warning("Expired cookie %r", value)
            return None
        
        try:
            return base64.b64decode(parts[0])
        except:
            return None
        
        
    
    def delete_cookie(self, name, path="/", domain=None):
        """Deletes the cookie with the given name.
        """
        
        self.response.set_cookie(
            name, 
            '', 
            path=path, 
            domain=domain, 
            max_age=0, 
            expires=datetime.timedelta(days=-5)
        )
        
    
    
    @property
    def current_user(self):
        """The authenticated user for this request.
        """
        
        if not hasattr(self, "_current_user"):
            self._current_user = self.get_current_user()
        return self._current_user
        
    
    def get_current_user(self):
        """Override to determine the current user from, e.g., a cookie.
        """
        
        return None
        
    
    
    @property
    def xsrf_token(self):
        """The XSRF-prevention token for the current user/session.
        """
        
        if not hasattr(self, "_xsrf_token"):
            token = self.get_cookie("_xsrf")
            if not token:
                token = binascii.b2a_hex(uuid.uuid4().bytes)
                expires_days = 30 if self.current_user else None
                self.set_cookie("_xsrf", token, expires_days=expires_days)
            self._xsrf_token = token
        return self._xsrf_token
        
    
    def check_xsrf_cookie(self):
        """Verifies that the '_xsrf' cookie matches the '_xsrf' argument.
        """
        
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return
        
        token = self.get_argument("_xsrf", None)
        if not token:
            raise HTTPError(403, "'_xsrf' argument missing from POST")
        if self.xsrf_token != token:
            raise HTTPError(403, "XSRF cookie does not match POST argument")
        
    
    def xsrf_form_html(self):
        """An HTML <input/> element to be included with all POST forms.
        """
        
        v = utils.xhtml_escape(self.xsrf_token)
        return '<input type="hidden" name="_xsrf" value="%s"/>' % v
        
    
    def static_url(self, path):
        """Returns a static URL for the given relative static file path.
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
                hashes[path] = hashlib.md5(f.read()).hexdigest()
                f.close()
        base = self.request.host_url
        static_url_prefix = self.settings.get('static_url_prefix', '/static/')
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
        
    
    
    def error(self, status=500, body=u'System Error'):
        """Clear response and return error.
        """
        
        self.response = webob.Response(status=status)
        
        if isinstance(body, unicode):
            self.response.unicode_body = body
        else:
            self.response.body = body
        
        return self.response
        
    
    def handle_exception(self, err):
        """Override to handle errors nicely.
        """
        
        logging.error(err, exc_info=True)
        return self.error()
        
    
    def handle_method_not_allowed(self, method_name):
        """Override to handle 405 nicely.
        """
        
        msg = u'%s method not allowed' % method_name
        
        logging.warning(msg)
        return self.error(status=405, body=msg)
        
    
    
    def render_template(self, tmpl_name, **kwargs):
        params = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html
        )
        kwargs.update(params)
        return template.render_tmpl(self.tmpl_lookup, tmpl_name, **kwargs)
        
    
    def redirect(self, url, status=302, content_type=None):
        """Handle redirecting.
        """
        
        self.response.status = status
        if not self.response.headerlist:
            self.response.headerlist = []
        self.response.headerlist.append(('Location', url))
        if content_type:
            self.response.content_type = content_type
        return self.response
        
    
    
    def _handle_method_not_found(self, method_name):
        """ Override to handle 405 nicely.
        """
        
        logging.warning(u'{} method not found'.format(method_name))
        return self.error(405)
        
    
    def _handle_system_error(self, err):
        """ Override to handle 500 nicely.
        """
        
        logging.error(err, exc_info=True)
        return self.error(500)
        
    
    
    def __call__(self, method_name, *groups):
        """
        """
        
        method = IMethodSelector(self).select_method(method_name)
        if method is None:
            handler_response = self._handle_method_not_found(method_name)
        else:
            try:
                handler_response = method(*groups)
            except Exception, err:
                handler_response = self._handle_system_error(err)
        
        if IResponse.providedBy(handler_response):
            self.response = handler_response
        elif isinstance(handler_response, str):
            self.response.body = handler_response
        elif isinstance(handler_response, unicode):
            self.response.unicode_body = handler_response
        elif handler_response is None: # leave self.response alone
            pass
        else: # assume it's json data
            self.response.content_type = 'application/json; charset=UTF-8'
            self.response.unicode_body = utils.json_encode(handler_response)
        
        return self.response
        
    
    

