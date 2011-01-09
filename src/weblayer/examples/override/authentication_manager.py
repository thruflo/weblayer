#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Example showing how to override the 
  :py:class:`~weblayer.interfaces.IAuthenticationManager` component.
  
"""

from zope.component import adapts
from zope.interface import implements

from weblayer import Bootstrapper, RequestHandler, WSGIApplication
from weblayer.interfaces import IAuthenticationManager, IRequest

class LazyAuthenticationManager(object):
    """ Assumes you're Brian.
    """
    
    adapts(IRequest)
    implements(IAuthenticationManager)
    
    def __init__(self, request):
        self.request = request
    
    is_authenticated = True
    current_user = {'display_name': 'Brian'}
    


class Hello(RequestHandler):
    def get(self):
        return u'Hello %s' % self.auth.current_user['display_name']
    


mapping = [(r'/.*', Hello)]

config = {
    'cookie_secret': '...', 
    'static_files_path': '/var/www/static',
    'template_directories': ['templates']
}

bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
application = WSGIApplication(
    *bootstrapper(AuthenticationManager=LazyAuthenticationManager)
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 8080, application).serve_forever()
