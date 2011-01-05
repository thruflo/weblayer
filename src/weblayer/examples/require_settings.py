#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" An example showing how to explicitly require settings.
"""

from weblayer import Bootstrapper, RequestHandler, WSGIApplication

class Hello(RequestHandler):
    def get(self, world):
        return u'hello {}'.format(world)
    


mapping = [(r'/(.*)', Hello)]

config = {
    'cookie_secret': '...',
    'static_files_path': '/var/www/static',
    'template_directories': ['/my/app/templates']
}

bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
application = WSGIApplication(*bootstrapper(require_settings=True))

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 8080, application).serve_forever()
