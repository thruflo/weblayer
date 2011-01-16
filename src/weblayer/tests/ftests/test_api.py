#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Functional tests for a :ref:`weblayer` application using the 
  :ref:`request handler api`.
"""

import unittest

class TestBasics(unittest.TestCase):
    """ Sanity check the basics of hooking up a request handler and returning
      a simple response.
    """
    
    def make_app(self, mapping):
        from os.path import dirname, join as join_path
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        _here = dirname(__file__)
        config = {
            'cookie_secret': 'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715d',
            'static_files_path': join_path(_here, 'static'),
            'template_directories': [join_path(_here, 'templates')]
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_hello_world(self):
        """ Can we hook up a request handler with a positional argument
          from the request path and return a simple response?
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self, world):
                return u'hello %s' % world
            
        
        
        mapping = [(r'/(.*)', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/world')
        
        self.assertTrue(res.body == 'hello world')
        
    
    def test_unicode_response(self):
        """ Can we return unicode characters?
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self):
                return u'hello Ð'
            
        
        
        mapping = [(r'/', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/')
        
        self.assertTrue(res.unicode_body == u'hello Ð')
        
    
    def test_mapping(self):
        """ Can we hook up multiple handlers?
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return 'a'
            
        
        class B(RequestHandler):
            def get(self):
                return 'b'
            
        
        
        mapping = [(
                r'/a',
                A
            ), (
                r'/.*',
                B
            )
        ]
        
        app = self.make_app(mapping)
        
        res = app.get('/a')
        self.assertTrue(res.body == 'a')
        
        res = app.get('/foobar')
        self.assertTrue(res.body == 'b')
        
    
    def test_groups(self):
        """ Each group in the request path should be passed as to the handler
          method as a positional argument.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self, *args):
                return ''.join(args)
            
        
        
        mapping = [(r'/(.)/(.)/(.)', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/a/b/c')
        
        self.assertTrue(res.body == 'abc')
        
    
    def test_head_method(self):
        """ HEAD requests should use ``Hander.get`` iff ``'head'`` is exposed,
          ``get()`` is defined and ``head()`` isn't.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self):
                return 'hello'
            
        
        
        mapping = [(r'/', Handler)]
        
        app = self.make_app(mapping)
        res = app.head('/')
        
        self.assertTrue(res.headers['Content-Length'] == '5')
        
    
    def test_form_post(self):
        """ POST requests should call ``Hander.post``.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            
            __all__ = ('get', 'post')
            
            def get(self):
                form = u'<form method="post"><input name="name" /></form>'
                return u'What is your name? %s' % form
                
            
            def post(self):
                return u'Hello %s!' % self.request.params.get('name')
                
            
            
        
        
        mapping = [(r'/', Handler)]
        app = self.make_app(mapping)
        
        res = app.get('/')
        form = res.form
        form['name'] = 'Brian'
        
        res = form.submit()
        self.assertTrue(res.body == 'Hello Brian!')
        
    
    


class TestResponse(unittest.TestCase):
    """ Sanity check response generation.
    """
    
    def make_app(self, mapping):
        from os.path import dirname, join as join_path
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        _here = dirname(__file__)
        config = {
            'cookie_secret': 'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715d',
            'static_files_path': join_path(_here, 'static'),
            'template_directories': [join_path(_here, 'templates')]
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_return_basestring(self):
        """ Returning a ``basestring`` from a request handler method should
          update the ``response.body``.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return 'hello'
            
        
        class B(RequestHandler):
            def get(self):
                return u'hellö'
            
        
        
        mapping = [(r'/a', A), (r'/b', B)]
        app = self.make_app(mapping)
        
        res = app.get('/a')
        self.assertTrue(res.body == 'hello')
        
        res = app.get('/b')
        self.assertTrue(res.unicode_body == u'hellö')
        
    
    def test_return_none(self):
        """ Returning ``None`` should fallback on ``self.response``.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                self.response.body = 'elephants'
                return None
            
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        res = app.get('/')
        self.assertTrue(res.body == 'elephants')
        
    
    def test_return_response(self):
        """ Returning an :py:class:`~weblayer.interfaces.IResponse` from a
          request handler method should overwrite and use ``self.response``.
        """
        
        from weblayer import RequestHandler
        from weblayer.base import Response
        
        class A(RequestHandler):
            def get(self):
                response = Response(body='fandango', request=self.request)
                response.environ['weblayer.test_return_response'] = 1
                return response
            
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        res = app.get('/', extra_environ={'weblayer.test_return_response': 0})
        self.assertTrue(res.body == 'fandango')
        self.assertTrue(res.environ['weblayer.test_return_response'])
        
    
    def test_return_data(self):
        """ Returning something other than a ``basestring``, ``None`` or
          :py:class:`~weblayer.interfaces.IResponse`` should JSON encode it.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return {'a': 'b'}
            
        
        
        class B(RequestHandler):
            def get(self):
                return {'a': u'ß'}
            
        
        
        mapping = [(r'/a', A), (r'/b', B)]
        app = self.make_app(mapping)
        
        res = app.get('/a')
        self.assertTrue(res.body == '{"a": "b"}')
        
        res = app.get('/b')
        self.assertTrue(res.unicode_body == u'{"a": "ß"}')
        
    
    


class TestSettings(unittest.TestCase):
    """ Sanity check ``self.settings``.
    """
    
    def make_app(self, config, mapping):
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_required_settings_misses_raises_error(self):
        """ You must provide required settings by default.
        """
        
        from weblayer import RequestHandler
        
        config = {}
        mapping = [(r'/', RequestHandler)]
        
        self.assertRaises(
            KeyError,
            self.make_app,
            config, 
            mapping
        )
        
        
    
    def test_settings_available(self):
        """ Settings are available as self.settings.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return '%s %s' % (
                    self.settings['cookie_secret'],
                    self.settings.get('not_present', None)
                )
            
        
        
        config = {
            'cookie_secret': '...',
            'static_files_path': 'static',
            'template_directories': ['templates']
        }
        mapping = [(r'/', A)]
        
        app = self.make_app(config, mapping)
        res = app.get('/')
        
        self.assertTrue(res.body == '... None')
        
    
    



"""
* ``self.auth``
* ``self.cookies``
* ``self.static``
* ``self.xsrf_input``
* return ``self.error()`` to return an HTTP error
* return ``self.redirect()`` to redirect the request
* return ``self.render()`` to return a rendered template

"""