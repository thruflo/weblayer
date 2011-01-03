#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" An example showing how to deploy a minimal weblayer application
  on `Google App Engine`_.
  
  .. _`Google App Engine`: # @@
"""

from google.appengine.ext.webapp.util import run_wsgi_app
from weblayer import Bootstrapper, RequestHandler, WSGIApplication

class Hello(RequestHandler):
    def get(self, world):
        return u'hello {}'.format(world)
    


# map urls to request handlers using regular expressions.
mapping = [(r'/(.*)', Hello)]

# your application settings (hardcoded for this example)
config = {
    'cookie_secret': '...',
    'static_files_path': '/var/www/static',
    'template_directories': ['/my/app/templates']
}

def main():
    bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
    run_wsgi_app(WSGIApplication(*bootstrapper()))
    

