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

raise NotImplementedError(
  """ Atm, scanning `@expose` decorated methods doesn't work
    with the order we bootstrap stuff.
    
    We can scan the packages fine.  The issue is if we've built
    a `url_mapping` beforehand then the classes in that aren't
    scanned.
    
    We could:
    
    * stop using an `@expose` decorator at all, expose the default
      set of HTTP verbs and provide default '405' handler methods
      for all the verbs -- this is simplest, removes the syntax
      headache but isn't as explicit.  Presumably we'd store the
      list of verbs in `__all__`, `__exposed_methods__`, which
      we would then allow the user to edit manually?
      
    * skip the venusian aspect of the decorator: there's no harm
      calling the `@expose` decorator more than once.  We would
      need to hack copy over some parts of the venusian internals
      to amend the class definition which is perhaps buggy but
      then perhaps not so bad.  Once done, this allows us to be
      explicit again.
      
    * change the pattern for the url_mapping to use dotted paths
      that we import when initialising the path_router
      
    * pass some sort of registry to the venusian scanner (n.b.:
      this is how it's meant to be used...)
    
  """
)

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
            import logging
            logging.warning(
                'scanner.scan({}, categories={})'.format(
                    item, 
                    categories
                )
            )
            
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
                required=[IRequirableSettings],
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
                required=[IRequest, IRequirableSettings],
                provided=IStaticURLGenerator
            )
        
        if SecureCookieWrapper is not False:
            if SecureCookieWrapper is None:
                SecureCookieWrapper = SignedSecureCookieWrapper
            registry.registerAdapter(
                SecureCookieWrapper, 
                required=[IRequest, IResponse, IRequirableSettings],
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
        
    
    def __call__(self, packages=None, scan_framework=True):
        """ `scan()` `setup_components()` and return `settings`, `path_router`.
        """
        
        if packages is None:
            packages = []
        
        if scan_framework:
            packages.append('thruflo.webapp')
        
        to_scan = []
        for item in packages:
            if not item in sys.modules:
                __import__(item)
            to_scan.append(sys.modules[item])
        
        self.scan(packages=to_scan)
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
        
    
    

