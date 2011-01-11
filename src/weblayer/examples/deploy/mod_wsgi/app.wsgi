#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A simple example showing how to deploy :ref:`weblayer` with 
  `Apache mod_wsgi`_.
  
  By default, `Apache mod_wsgi`_ looks for a callable WSGI application
  entry point called ``application`` in a ``.wsgi`` file hooked up with
  the `WSGIScriptAlias` directive, e.g.::
  
      WSGIScriptAlias / /path/to/app.wsgi
  
  See `this page`_ for a quick configuration guide explaining how to setup
  `Apache mod_wsgi`_.
  
  .. _`Apache mod_wsgi`: http://code.google.com/p/modwsgi
  .. _`this page`: http://code.google.com/p/modwsgi/wiki/QuickConfigurationGuide
"""

from weblayer import Bootstrapper, RequestHandler, WSGIApplication

class Hello(RequestHandler):
    def get(self, world):
        return u'hello %s' % world
    


mapping = [(r'/(.*)', Hello)]

config = {
    'cookie_secret': '...', 
    'static_files_path': '/var/www/static',
    'template_directories': ['templates']
}

bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
application = WSGIApplication(*bootstrapper())
