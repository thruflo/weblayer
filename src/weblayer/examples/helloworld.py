#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A simple hello world example.
"""

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
    """ Serve on port 8000.
    """
    
    from wsgiref.simple_server import make_server
    wsgi_server = make_server('', 8080, app_factory())
    
    try:
        wsgi_server.serve_forever()
    except KeyboardInterrupt:
        pass
        
    


if __name__ == '__main__':
    main()

