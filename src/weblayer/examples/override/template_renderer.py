#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Example showing how to override the 
  :py:class:`~weblayer.interfaces.ITemplateRenderer` component.
  
"""

from zope.component import adapts
from zope.interface import implements

from weblayer import Bootstrapper, RequestHandler, WSGIApplication
from weblayer.interfaces import ISettings, ITemplateRenderer
from weblayer.utils import xhtml_escape

class LazyTemplateRenderer(object):
    """ Echos the `tmpl_name`, `kwargs` and `settings`.
    """
    
    adapts(ISettings)
    implements(ITemplateRenderer)
    
    def __init__(self, settings, **kwargs):
        self.settings = settings
    
    
    def render(self, tmpl_name, **kwargs):
        return u'<h2>%s</h2><p>%s</p><p>%s</p>' % (
            tmpl_name, 
            xhtml_escape(unicode(kwargs)),
            xhtml_escape(unicode(self.settings))
        )
    
    


class Hello(RequestHandler):
    def get(self, world):
        return self.render('hello.tmpl', world=world)
    


mapping = [(r'/(.*)', Hello)]

config = {
    'cookie_secret': '...', 
    'static_files_path': '/var/www/static',
    'template_directories': ['templates']
}

bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
application = WSGIApplication(
    *bootstrapper(TemplateRenderer=LazyTemplateRenderer)
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 8080, application).serve_forever()
