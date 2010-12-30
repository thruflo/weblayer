#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" An example showing how to deploy a minimal weblayer application
  on `Google App Engine`_.
  
  .. _`Google App Engine`: # @@
"""

from google.appengine.ext.webapp.util import run_wsgi_app
from weblayer import Bootstrapper, RequestHandler, WSGIApplication

class Hello(RequestHandler):
    """ An example request handler, aka view class.
    """
    
    def get(self, world):
        return u'hello {}'.format(world)
        
    
    


# map urls to request handlers using regular expressions.
url_mapping = [(r'/(.*)', Hello)]

# your application settings (hardcoded for this example)
app_settings = {
    'cookie_secret': '...',
    'static_files_path': '/var/www/static',
    'template_directories': ['/my/app/templates']
}

def app_factory():
    """ Bootstrap and return a `WSGIApplication`.
    """
    
    bootstrapper = Bootstrapper(settings=app_settings, url_mapping=url_mapping)
    settings, path_router = bootstrapper()
    return WSGIApplication(settings, path_router)
    


def main():
    """ Static main function is called by app engine
    """
    
    application = app_factory()
    run_wsgi_app(application)
    

