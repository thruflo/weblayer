#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Template rendering.
"""

import datetime

from zope.interface import implements
from mako.lookup import TemplateLookup

from interfaces import ITemplateRenderer
import utils

DEFAULT_BUILT_INS = {
    "escape": utils.xhtml_escape,
    "url_escape": utils.url_escape,
    "json_encode": utils.json_encode,
    "squeeze": utils.squeeze,
    "datetime": datetime,
}

class MakoTemplateRenderer(object):
    """ `Mako` template renderer.
    """
    
    implements(ITemplateRenderer)
    
    def __init__(
            self, 
            directories,
            built_ins=DEFAULT_BUILT_INS,
            module_directory='/tmp/mako_modules',
            input_encoding='utf-8', 
            output_encoding='utf-8', 
            encoding_errors='replace',
            **kwargs
        ):
        """
        """
        
        self.built_ins = DEFAULT_BUILT_INS
        self.template_lookup = TemplateLookup(
            directories=directories,
            module_directory=module_directory,
            input_encoding=input_encoding, 
            output_encoding=output_encoding, 
            encoding_errors=encoding_errors,
            **kwargs
        )
        
    
    def render(self, tmpl_name, **kwargs):
        """ Render `tmpl_name`, unpacking `self.built_ins` and `kwargs`
          into the template's global namespace.
        """
        
        params = self.built_ins.copy()
        params.update(kwargs)
        
        t = self.template_lookup.get_template(tmpl_name)
        return t.render(**params)
        
    
    

