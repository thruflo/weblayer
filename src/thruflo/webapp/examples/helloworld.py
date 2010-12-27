#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A simple hello world example.
"""

from thruflo.webapp import Bootstrapper, RequestHandler, WSGIApplication

class Hello(RequestHandler):
    """ An example request handler, aka view class.
    """
    
    def get(self, world):
        return u'hello {}'.format(world)
        
    
    


url_mapping = [(r'/(.*)', Hello)]

app_settings = {
    'cookie_secret': '...',
    'static_files_path': '/var/www/static',
    'template_directories': ['/my/app/templates']
}

def app_factory():
    bootstrapper = Bootstrapper(settings=app_settings, url_mapping=url_mapping)
    settings, path_router = bootstrapper()
    return WSGIApplication(settings, path_router)
    


if __name__ == '__main__':
    from paste.httpserver import serve
    application = app_factory()
    try:
        serve(application)
    except KeyboardInterrupt:
        pass
        
    

