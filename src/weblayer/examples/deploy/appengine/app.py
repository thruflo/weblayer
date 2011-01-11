#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" An example showing how to deploy a minimal weblayer application
  on `Google App Engine`_.
  
  Note that you must have :ref:`weblayer` and its dependencies included 
  in :py:obj:`sys.path`, e.g.: by copying them into this folder.  Check the
  ``install_requires`` list in ``setup.py`` but at the time of writing this
  means you need to include:
  
  * `mako`, 
  * `venusian`, 
  * `weblayer`, 
  * `webob`, 
  * `zope.component`
  * `zope.interface`
  * `zope.event`
  * `pkg_resources.py`
  
  .. _`Google App Engine`: http://code.google.com/appengine/
"""

from google.appengine.ext.webapp.util import run_wsgi_app
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

def main():
    bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
    run_wsgi_app(WSGIApplication(*bootstrapper()))
