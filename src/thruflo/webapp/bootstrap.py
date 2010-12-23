#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Provides `Bootstrapper`, a helper class that simplifies bootstrapping
  application components.
"""

__all__ = [
    'Bootstrapper'
]

import inspect
import sys

from os.path import dirname

import venusian

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
    """ Bootstrap thruflo.webapp components.
      
      To bootstrap a default configuration, pass a dictionary of settings
      and list of url mappings to the constructor::
      
          bootstrapper = Bootstrapper(settings={}, url_mapping=[])
      
      Then call the instance to:
      
      * scan for venusian callbacks
      * register components
      * get IRequirableSettings and IPathRouter utilities
      
      ::
      
          settings, path_router = bootstrapper()
      
    """
    
    def scan(
            self, 
            packages=None, 
            extra_categories=None,
            settings=None
        ):
        """ Run a `venusian` scan on packages.
        """
        
        if not packages:
            return
        
        if settings is None:
            scanner = venusian.Scanner(settings=self._settings)
        else:
            scanner = venusian.Scanner(settings=settings)
        
        categories = ['thruflo.webapp']
        if extra_categories is not None:
            categories.extend(extra_categories)
        
        for item in packages:
            scanner.scan(item, categories=categories)
        
        return scanner
        
    
    def setup_components(
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
                self._settings(self._user_settings)
                settings = self._settings
            registry.registerUtility(settings, IRequirableSettings)
        
        if path_router is not False:
            if path_router is None:
                path_router = RegExpPathRouter(self._url_mapping)
            registry.registerUtility(path_router, IPathRouter)
        
        if TemplateRenderer is not False:
            if TemplateRenderer is None:
                TemplateRenderer = MakoTemplateRenderer
            registry.registerAdapter(
                TemplateRenderer, 
                adapts=[IRequirableSettings],
                provides=ITemplateRenderer
            )
        
        if AuthenticationManager is not False:
            if AuthenticationManager is None:
                AuthenticationManager = TrivialAuthenticationManager
            registry.registerAdapter(
                AuthenticationManager, 
                adapts=[IRequestHandler],
                provides=IAuthenticationManager
            )
        
        if StaticURLGenerator is not False:
            if StaticURLGenerator is None:
                StaticURLGenerator = MemoryCachedStaticURLGenerator
            registry.registerAdapter(
                StaticURLGenerator, 
                adapts=[IRequest, IRequirableSettings],
                provides=IStaticURLGenerator
            )
        
        if SecureCookieWrapper is not False:
            if SecureCookieWrapper is None:
                SecureCookieWrapper = SignedSecureCookieWrapper
            registry.registerAdapter(
                SecureCookieWrapper, 
                adapts=[IRequest, IResponse, IRequirableSettings],
                provides=ISecureCookieWrapper
            )
        
        if MethodSelector is not False:
            if MethodSelector is None:
                MethodSelector = ExposedMethodSelector
            registry.registerAdapter(
                MethodSelector, 
                adapts=[IRequestHandler],
                provides=IMethodSelector
            )
        
        if ResponseNormaliser is not False:
            if ResponseNormaliser is None:
                ResponseNormaliser = DefaultToJSONResponseNormaliser
            registry.registerAdapter(
                ResponseNormaliser, 
                adapts=[IResponse],
                provides=IResponseNormaliser
            )
        
    
    def __call__(self, packages=None, scan_caller=True, scan_framework=True):
        """ `scan()` `setup_components()` and return `settings`, `path_router`.
        """
        
        if packages is None:
            packages = []
        
        if scan_caller:
            calling_mod = inspect.getmodule(inspect.stack()[1][0])
            packages.append(dirname(calling_mod.__file__))
            
        if scan_framework:
            packages.append(sys.modules['thruflo.webapp'])
        
        self.scan(packages=packages)
        self.setup_components()
        
        settings = registry.getUtility(IRequirableSettings)
        path_router = registry.getUtility(IPathRouter)
        
        return settings, path_router
        
    
    def __init__(self, settings=None, url_mapping=None):
        """ Stores the `settings` and `url_mapping` provided and initialises
          a `RequirableSettings` instance.
        """
        
        if settings is None:
            self._user_settings = {}
        else:
            self._user_settings = settings
        
        if url_mapping is None:
            self._url_mapping = []
        else:
            self._url_mapping = url_mapping
        
        self._settings = RequirableSettings()
        
    
    

