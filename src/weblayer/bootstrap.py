#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Provides `Bootstrapper`, a helper class that simplifies setting up
  and registering `weblayer` components.
"""

__all__ = [
    'Bootstrapper'
]

import sys

from component import registry
from interfaces import *

from auth import TrivialAuthenticationManager
from cookie import SignedSecureCookieWrapper
from method import ExposedMethodSelector
from normalise import DefaultToJSONResponseNormaliser
from route import RegExpPathRouter
from settings import RequirableSettings
from static import MemoryCachedStaticURLGenerator
from template import MakoTemplateRenderer

class Bootstrapper(object):
    """ Bootstrap `weblayer` components.
      
      To bootstrap a default configuration, pass a dictionary of settings
      and list of url mappings to the constructor::
      
          >>> _settings = {'cookie_secret': '', 'template_directories': []}
          >>> bootstrapper = Bootstrapper(settings=_settings, url_mapping=[])
      
      Then call the instance to scan for registered settings, register 
      components and get ISettings and IPathRouter utilities::
      
          >>> settings, path_router = bootstrapper()
      
      This will raise a `KeyError` if the required settings aren't passed in::
      
          >>> bootstrapper = Bootstrapper(settings={}, url_mapping=[])
          >>> settings, path_router = bootstrapper() #doctest: +NORMALIZE_WHITESPACE
          Traceback (most recent call last):
          ...
          KeyError: u'Required setting `template_directories` () is missing, 
                    Required setting `cookie_secret` (a long, random sequence 
                    of bytes) is missing'
          
      Unless you tell it not to scan the framework (and don't pass in any other
      packages to scan)::
      
          >>> settings, path_router = bootstrapper(scan_framework=False)
      
    """
    
    def require_settings(
            self, 
            packages=None, 
            scan_framework=True, 
            extra_categories=None
        ):
        """ Init and return `RequirableSettings`, scanning 
          `packages` for required settings in the process.
        """
        
        if packages is None:
            packages = []
        
        if scan_framework:
            packages.insert(0, 'weblayer')
        
        to_scan = []
        for item in packages:
            if not item in sys.modules: # pragma: no coverage
                __import__(item)
            to_scan.append(sys.modules[item])
        
        
        settings = RequirableSettings(
            packages=to_scan,
            extra_categories=extra_categories
        )
        return settings
        
    
    def register_components(
            self, 
            settings=None,
            path_router=None,
            TemplateRenderer=None,
            AuthenticationManager=None, 
            SecureCookieWrapper=None, 
            StaticURLGenerator=None,
            MethodSelector=None,
            ResponseNormaliser=None
        ):
        """ Setup component registrations. Pass in alternative implementations
          here to override, or `False` to avoid registering a component.
        """
        
        if settings is not False:
            if settings is None:
                settings = RequirableSettings()
            settings(self._user_settings)
            registry.registerUtility(settings, ISettings)
        
        if path_router is not False:
            if path_router is None:
                path_router = RegExpPathRouter(self._url_mapping)
            registry.registerUtility(path_router, IPathRouter)
        
        if TemplateRenderer is not False:
            if TemplateRenderer is None:
                TemplateRenderer = MakoTemplateRenderer
            registry.registerAdapter(
                TemplateRenderer, 
                required=[ISettings],
                provided=ITemplateRenderer
            )
        
        if AuthenticationManager is not False:
            if AuthenticationManager is None:
                AuthenticationManager = TrivialAuthenticationManager
            registry.registerAdapter(
                AuthenticationManager, 
                required=[IRequest],
                provided=IAuthenticationManager
            )
        
        if StaticURLGenerator is not False:
            if StaticURLGenerator is None:
                StaticURLGenerator = MemoryCachedStaticURLGenerator
            registry.registerAdapter(
                StaticURLGenerator, 
                required=[IRequest, ISettings],
                provided=IStaticURLGenerator
            )
        
        if SecureCookieWrapper is not False:
            if SecureCookieWrapper is None:
                SecureCookieWrapper = SignedSecureCookieWrapper
            registry.registerAdapter(
                SecureCookieWrapper, 
                required=[IRequest, IResponse, ISettings],
                provided=ISecureCookieWrapper
            )
        
        if MethodSelector is not False:
            if MethodSelector is None:
                MethodSelector = ExposedMethodSelector
            registry.registerAdapter(
                MethodSelector, 
                required=[IRequestHandler],
                provided=IMethodSelector
            )
        
        if ResponseNormaliser is not False:
            if ResponseNormaliser is None:
                ResponseNormaliser = DefaultToJSONResponseNormaliser
            registry.registerAdapter(
                ResponseNormaliser, 
                required=[IResponse],
                provided=IResponseNormaliser
            )
        
    
    
    def __call__(
            self, 
            require_settings=False,
            packages=None, 
            scan_framework=True, 
            extra_categories=None,
            **kwargs
        ):
        """ if `require_settings` is `True, call :py:meth:`require_settings`, 
          :py:meth:`register_components` and return `settings, path_router`.
        """
        
        if not require_settings or 'settings' in kwargs:
            settings_component = kwargs.get('settings', None)
        else:
            settings_component = self.require_settings(
                packages=packages,
                scan_framework=scan_framework,
                extra_categories=extra_categories
            )
        
        kwargs['settings'] = settings_component
        self.register_components(**kwargs)
        
        settings = registry.getUtility(ISettings)
        path_router = registry.getUtility(IPathRouter)
        
        return settings, path_router
        
    
    def __init__(self, settings=None, url_mapping=None):
        """ Stores the `settings` and `url_mapping` provided.
        """
        
        if settings is None:
            self._user_settings = {}
        else:
            self._user_settings = settings
        
        if url_mapping is None:
            self._url_mapping = []
        else:
            self._url_mapping = url_mapping
        
    
    

