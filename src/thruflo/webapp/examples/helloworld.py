#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A simple hello world example.
"""

from thruflo.webapp import Bootstrapper, RequestHandler, WSGIApplication

class Hello(RequestHandler):
    def get(self, world):
        return u'hello {}'.format(world)
    


url_mapping = [(r'/(.*)', Hello)]

app_settings = {
    'cookie_secret': '...',
    'static_files_path': '/var/www/static',
    'template_directories': ['/my/app/templates']
}

if __name__ == '__main__':
    bootstrapper = Bootstrapper(app_settings, url_mapping)
    application = WSGIApplication(*bootstrapper())
    
    from paste.httpserver import serve
    try:
        serve(application)
    except KeyboardInterrupt:
        pass
        
    

