#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `Interface`_ definitions.
  
  .. _`Interface`: http://pypi.python.org/pypi/zope.interface
"""

from zope.interface import Interface, Attribute

class ITemplateRenderer(Interface):
    """ A utility which renders templates.
    """
    
    def render(tmpl_name, **kwargs):
        """ Render a template identified with `tmpl_name`.
        """
        
    
    

