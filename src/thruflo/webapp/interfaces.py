#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" `Interface`_ definitions.
  
  .. _`Interface`: http://pypi.python.org/pypi/zope.interface
"""

from zope.interface.interface import Interface, Method #, Attribute

class ITemplateRenderer(Interface):
    """
    """
    
    render = Method(u'Render a template')
    


