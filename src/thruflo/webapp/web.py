#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Yet another WSGI framework::
  
      import web
      
      class MainPage(web.RequestHandler):
          def get(self):
              return 'hello world'
              
          
      
      mapping = [('/.*', MainPage)]
      application = web.WSGIApplication(mapping)
      
    
  Based on WebOb.  RegExp URL mapping ala app engine's webapp.
  Some RequestHandler methods borrowed from Tornado.
  
"""

import base64
import binascii
import calendar
import cgi
import Cookie
import datetime
import email.utils
import hashlib
import hmac
import httplib
import logging
import os
import re
import time
import uuid

from os.path import dirname, join as join_path

import webob

import template
import utils

RE_FIND_GROUPS = re.compile('\(.*?\)')
_CHARSET_RE = re.compile(r';\s*charset=([^;\s]*)', re.I)

SUPPORTED_METHODS = [
    'HEAD', 
    'GET', 
    'PUT', 
    'POST', 
    'DELETE'
]

DEFAULT_SETTINGS = {
    'static_path': join_path(os.getcwd(), 'static'),
    'tmpl_dirs': [join_path(os.getcwd(), 'templates')],
    'cookie_secret': 'ONqi04WSTsqnYjznTRZeH3d5lhi6pULqiGgRdGy9GIE=',
    'login_url': '/login',
    'xsrf_cookies': True
}

class WSGIApplication(object):
    """Wraps a set of RequestHandlers in a WSGI-compatible application.
    """
    
    def __init__(self, url_mapping, settings={}):
        """Initializes with the given URL mapping.
        """
        
        self._init_url_mappings(url_mapping)
        self.settings = DEFAULT_SETTINGS
        self.settings.update(settings)
        self.tmpl_lookup = template.tmpl_lookup_factory(
            settings['tmpl_dirs']
        )
        self.current_request_args = ()
        
    
    
    def __call__(self, environ, start_response):
        """Called when a request comes in.
        """
        
        request = webob.Request(environ)
        response = webob.Response(
            status=200, 
            content_type='text/html; charset=UTF-8'
        )
        
        handler = None
        groups = ()
        for regexp, handler_class in self._url_mapping:
            match = regexp.match(request.path)
            if match:
                handler = handler_class(
                    request, 
                    response, 
                    self.settings, 
                    self.tmpl_lookup
                )
                groups = match.groups()
                break
                
        self.current_request_args = groups
        
        if handler:
            method_name = environ['REQUEST_METHOD']
            if method_name in SUPPORTED_METHODS:
                method = getattr(handler, method_name.lower(), None)
                if method:
                    try:
                        handler_response = method(*groups)
                    except Exception, err:
                        response = handler.handle_exception(err)
                    else:
                        if isinstance(handler_response, webob.Response):
                            response = handler_response
                        elif isinstance(handler_response, str):
                            response.body = handler_response
                        elif isinstance(handler_response, unicode):
                            response.unicode_body = handler_response
                        else: # assume it's data
                            response.content_type = 'application/json; charset=UTF-8'
                            response.unicode_body = utils.json_encode(handler_response)
                else:
                    response.status = 405
            else:
                response.status = 405
        else:
            response.status = 404
        
        return response(environ, start_response)
        
    
    
    def _init_url_mappings(self, handler_tuples):
        """Initializes mapping urls to handlers and handlers to urls.
        """
        
        handler_map = {}
        pattern_map = {}
        url_mapping = []
        
        for regexp, handler in handler_tuples:
            try:
                handler_name = handler.__name__
            except AttributeError:
                pass
            else:
                handler_map[handler_name] = handler
            
            if not regexp.startswith('^'):
                regexp = '^' + regexp
            if not regexp.endswith('$'):
                regexp += '$'
            
            compiled = re.compile(regexp)
            url_mapping.append((compiled, handler))
            
            num_groups = len(RE_FIND_GROUPS.findall(regexp))
            handler_patterns = pattern_map.setdefault(handler, [])
            handler_patterns.append((compiled, num_groups))
        
        self._handler_map = handler_map
        self._pattern_map = pattern_map
        self._url_mapping = url_mapping
        
    
    
    def get_registered_handler_by_name(self, handler_name):
        """Returns the handler given the handler's name.
        """
        
        try:
            return self._handler_map[handler_name]
        except Exception:
            logging.error('Handler does not map to any urls: %s', handler_name)
            raise
        
    
    


class RequestHandler(object):
    """Provides ``self.settings``, ``self.current_user``, ``self.account``, 
      secure cookies, ``static_url()`` and ``xsrf_form_html()``.
    """
    
    def __init__(self, request, response, settings, tmpl_lookup):
        self.request = request
        self.response = response
        self.settings = settings
        self.tmpl_lookup = tmpl_lookup
        
    
    
    @property
    def cookies(self):
        """A dictionary of Cookie.Morsel objects.
        """
        
        return self.request.cookies
        
    
    def get_cookie(self, name, default=None):
        """Gets the value of the cookie with the given name, else default.
        """
        
        return self.request.cookies.get(name, default)
        
    
    def set_cookie(
            self, 
            name, 
            value, 
            domain=None, 
            expires=None, 
            path="/", 
            expires_days=None, 
            override=False
        ):
        """Sets the given cookie name/value with the given options.
        """
        
        name = _utf8(name)
        value = _utf8(value)
        
        if re.search(r"[\x00-\x20]", name + value):
            # Don't let us accidentally inject bad stuff
            raise ValueError("Invalid cookie %r: %r" % (name, value))
        
        max_age = None
        if expires_days:
            max_age = expires_days * 24 * 60 * 60
        
        if override:
            self.response.unset_cookie(name, strict=False)
        
        self.response.set_cookie(
            name, 
            value=value,
            path=path, 
            domain=domain, 
            expires=expires, 
            max_age=max_age
        )
        
    
    def clear_cookie(self, name, path="/", domain=None):
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
        self.set_cookie(
            name,
            value, 
            expires_days=expires_days, 
            **kwargs
        )
        
    
    def get_secure_cookie(self, name, include_name=True, value=None):
        """Returns the given signed cookie if it validates, or None.
        """
        
        if value is None: value = self.get_cookie(name)
        if not value: return None
        parts = value.split("|")
        if len(parts) != 3: return None
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
        
    
    
    def get_argument(self, name, default=None, strip=True):
        args = self.get_arguments(name, strip=strip)
        if not args:
            return default
        return args[-1]
        
    
    def get_arguments(self, name, strip=True):
        values = self.request.params.get(name, [])
        if not bool(isinstance(values, list) or isinstance(values, tuple)):
           values = [values]
        if strip:
            values = [x.strip() for x in values]
        return values
        
    
    
    def error(self, status=500, body='System Error'):
        """Clear response and return error.
        """
        
        self.response = webob.Response(status=status)
        self.response.body = body
        
        return self.response
        
    
    def handle_exception(self, err):
        """Override to handle errors nicely
        """
        
        logging.error(err, exc_info=True)
        return self.error()
        
    
    
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
        
    
    


def _utf8(s):
    if isinstance(s, unicode):
        return s.encode("utf-8")
    assert isinstance(s, str)
    return s
    

def _unicode(s):
    if isinstance(s, str):
        try:
            return s.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("Non-utf8 argument")
    assert isinstance(s, unicode)
    return s
    

def _time_independent_equals(a, b):
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0
    

