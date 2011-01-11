#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" :py:mod:`weblayer.component` provides ``registry``, an instance of
  a `zope.component.registry.Components`_ component management registry.
  
  ``registry`` provides methods to register and lookup `utilities`_ and
  `adapters`_ against :py:mod:`~weblayer.interfaces`.  For example::
  
      >>> from mock import Mock
      >>> from weblayer.interfaces import *
      >>> mock_path_router = Mock()
      >>> MockTemplateRenderer = Mock()
      >>> MockTemplateRenderer.return_value = 'mock_template_renderer'
  
  To register a utility::
  
      >>> registry.registerUtility(mock_path_router, IPathRouter)
  
  To register an adapter::
  
      >>> registry.registerAdapter(
      ...     MockTemplateRenderer, 
      ...     required=[ISettings],
      ...     provided=ITemplateRenderer
      ... )
  
  To get a registered utility::
  
      >>> path_router = registry.getUtility(IPathRouter)
      >>> path_router == mock_path_router
      True
  
  To get a registered adapter::
  
      >>> from weblayer.settings import RequirableSettings
      >>> settings = RequirableSettings()
      >>> template_renderer = registry.getAdapter(
      ...     settings, 
      ...     ITemplateRenderer
      ... )
  
  Note how you register an adapter class and get an instance::
  
      >>> MockTemplateRenderer.assert_called_with(settings)
      >>> template_renderer = 'mock_template_renderer'
  
  Tear down::
  
      >>> registry.unregisterUtility(provided=IPathRouter)
      True
      >>> registry.unregisterAdapter(
      ...     required=[ISettings], 
      ...     provided=ITemplateRenderer
      ... )
      True
  
  .. _`zope.component.registry.Components`: http://pypi.python.org/pypi/zope.component#component-management-objects
  .. _`utilities`: http://pypi.python.org/pypi/zope.component#id6
  .. _`adapters`: http://pypi.python.org/pypi/zope.component#id7
  
"""

from zope.component.registry import Components
registry = Components('weblayer')
