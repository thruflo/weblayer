#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" :py:mod:`weblayer.template` provides :py:class:`MakoTemplateRenderer`, an
  implementation of :py:class:`~weblayer.interfaces.ITemplateRenderer` that 
  uses `Mako`_ templates.
  
      >>> import tempfile, os
      >>> from os.path import basename, dirname
      >>> fd, abs_path = tempfile.mkstemp()
      >>> sock = os.fdopen(fd, 'w')
      >>> tmpl_dir = dirname(abs_path)
      >>> tmpl_name = basename(abs_path)
  
  :py:class:`MakoTemplateRenderer` requires 
  ``settings['template_directories']``::
  
      >>> settings = {'template_directories': [tmpl_dir]}
      >>> template_renderer = MakoTemplateRenderer(settings)
  
  And provides a :py:meth:`~MakoTemplateRenderer.render` method that accepts
  a ``tmpl_name`` which is resolved relative to
  ``settings['template_directories']`` and passes through a set of built in
  functions and the keyword arguments provided to 
  :py:meth:`~MakoTemplateRenderer.render` to the template's global namespace::
  
      >>> tmpl = u'<h1>${escape(foo)}</h1>'
      >>> sock.write(tmpl)
      >>> sock.close()
      >>> template_renderer.render(tmpl_name, foo='&')
      '<h1>&amp;</h1>'
  
  The built ins available by default are::
  
      DEFAULT_BUILT_INS = {
          "escape": utils.xhtml_escape,
          "url_escape": utils.url_escape,
          "json_encode": utils.json_encode,
          "datetime": datetime
      }
  
  Cleanup::
  
      >>> os.unlink(abs_path)
  
  .. _`Mako`: http://www.makotemplates.org/
"""

__all__ = [
    'MakoTemplateRenderer'
]

import datetime
import utils

from zope.component import adapts
from zope.interface import implements

from mako.lookup import TemplateLookup

from interfaces import ISettings, ITemplateRenderer
from settings import require_setting

DEFAULT_BUILT_INS = {
    "escape": utils.xhtml_escape,
    "url_escape": utils.url_escape,
    "json_encode": utils.json_encode,
    "datetime": datetime
}

require_setting('template_directories')

class MakoTemplateRenderer(object):
    """ `Mako <http://www.makotemplates.org/>`_ template renderer.
    """
    
    adapts(ISettings)
    implements(ITemplateRenderer)
    
    def __init__(
            self, 
            settings,
            built_ins=None,
            template_lookup_class=None,
            module_directory='/tmp/mako_modules',
            input_encoding='utf-8', 
            output_encoding='utf-8', 
            encoding_errors='replace',
            **kwargs
        ):
        """
        """
        
        directories = settings['template_directories']
        
        self.built_ins = built_ins is None and DEFAULT_BUILT_INS or built_ins
        
        if template_lookup_class is None:
            template_lookup_class = TemplateLookup
        
        self.template_lookup = template_lookup_class(
            directories=directories,
            module_directory=module_directory,
            input_encoding=input_encoding, 
            output_encoding=output_encoding, 
            encoding_errors=encoding_errors,
            **kwargs
        )
        
    
    def render(self, tmpl_name, **kwargs):
        """ Render ``tmpl_name``, unpacking ``self.built_ins`` and ``kwargs``
          into the template's global namespace.
        """
        
        params = self.built_ins.copy()
        params.update(kwargs)
        
        t = self.template_lookup.get_template(tmpl_name)
        return t.render(**params)
        
    
    

