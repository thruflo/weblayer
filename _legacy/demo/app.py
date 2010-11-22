#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Provides a WSGI app as ``application``.  You could run this 
  with ``./bin/thruflo-webapp-demo`` which calls ``main()`` or 
  using something like PasteScript_ or Gunicorn_.
  
  _PasteScript: http://pypi.python.org/pypi/PasteScript
  _Gunicorn: http://gunicorn.org/
"""

from os.path import dirname, join as join_path
from wsgiref.simple_server import make_server

from thruflo.webapp import web

class Index(web.RequestHandler):
    def get(self):
        return '<a href="/a?bar=b&baz=c">foo</a>'
        
    
    

class Foo(web.RequestHandler):
    """A request like ``/a?bar=b&baz=c`` will pass
      ``foo=a, bar=b, baz=c`` through to the template.
    """
    
    def get(self, foo):
        # use ``self.get_argument`` to read form params
        bar = self.get_argument('bar', None)
        # or use ``self.request.params.get`` directly
        baz = self.request.params.get('baz', None)
        # return the rendered template
        kwargs = {'foo': foo, 'bar': bar, 'baz': baz}
        return self.render_template('foo.tmpl', **kwargs)
        
    
    


settings = {
    'tmpl_dirs': [
        join_path(dirname(__file__), 'templates')
    ]
}
mapping = [(
        '/', 
        Index
    ), (
        '/([\w]*)\/?', 
        Foo
    )
]

def app_factory():
    return web.WSGIApplication(mapping, settings=settings)

application = app_factory()

def main():
    """Serve demo on port 8000.
    """
    
    wsgi_server = make_server('', 8000, application)
    
    try:
        wsgi_server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    


if __name__ == '__main__':
    main()

