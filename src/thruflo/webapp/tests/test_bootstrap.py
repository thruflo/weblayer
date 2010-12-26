#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit and integration tests for `thruflo.webapp.method`.
"""

import unittest
from mock import Mock

class TestInitBootstrapper(unittest.TestCase):
    """ Test the logic of `Bootstrap.__init__`.
    """
    
    def make_one(self, *args, **kwargs):
        from thruflo.webapp.bootstrap import Bootstrapper
        return Bootstrapper(*args, **kwargs)
        
    
    
    def test_init_settings(self):
        """ `settings` is available as `self._user_settings`.
        """
        
        settings = Mock()
        bootstrapper = self.make_one(settings=settings)
        self.assertTrue(bootstrapper._user_settings == settings)
        
    
    def test_init_url_map(self):
        """ `settings` is available as `self._user_settings`.
        """
        
        url_mapping = Mock()
        bootstrapper = self.make_one(url_mapping=url_mapping)
        self.assertTrue(bootstrapper._url_mapping == url_mapping)
        
    
    def test_init_requirable_settings(self):
        """ A `RequirableSettings` instance is constructed as `self._settings`.
        """
        
        from thruflo.webapp import bootstrap
        __RequirableSettings = bootstrap.RequirableSettings
        
        MockSettings = Mock()
        MockSettings.return_value = 'requirable settings'
        bootstrap.RequirableSettings = MockSettings
        
        bootstrapper = self.make_one()
        self.assertTrue(bootstrapper._settings == 'requirable settings')
        
        bootstrap.RequirableSettings = __RequirableSettings
    
    

class TestCallBootstrapper(unittest.TestCase):
    """ Test the logic of `Bootstrap.__call__`.
    """
    
    def setUp(self):
        from thruflo.webapp import bootstrap
        self.__inspect = bootstrap.inspect
        self.__dirname = bootstrap.dirname
        self.__sys = bootstrap.sys
        self.__registry = bootstrap.registry
        self.inspect = Mock()
        self.calling_module = Mock()
        self.calling_module.__file__ = '/foo/bar.py'
        self.inspect.getmodule.return_value = self.calling_module
        self.inspect.stack.return_value = ['', ['']]
        self.dirname = Mock()
        self.dirname.return_value = '/foo/bar'
        self.sys = Mock()
        self.sys.modules = {'thruflo.webapp': 'thruflo.webapp package'}
        self.registry = Mock()
        self.registry.getUtility.return_value = 'registered utility'
        bootstrap.inspect = self.inspect
        bootstrap.dirname = self.dirname
        bootstrap.sys = self.sys
        bootstrap.registry = self.registry
        
    
    def tearDown(self):
        from thruflo.webapp import bootstrap
        bootstrap.inspect = self.__inspect
        bootstrap.dirname = self.__dirname
        bootstrap.sys = self.__sys
        bootstrap.registry = self.__registry
        
    
    def make_one(self, *args, **kwargs):
        from thruflo.webapp.bootstrap import Bootstrapper
        bootstrapper = Bootstrapper(*args, **kwargs)
        bootstrapper.scan = Mock()
        bootstrapper.setup_components = Mock()
        return bootstrapper
        
    
    def test_scan_framework_appends_thruflo_webapp_to_packages(self):
        """ When `scan_framework` is `True`, we append
          `sys.modules['thruflo.webapp']` to packages.
        """
        
        bootstrapper = self.make_one()
        bootstrapper(packages=[], scan_framework=True)
        packages = bootstrapper.scan.call_args[1]['packages']
        self.assertTrue('thruflo.webapp package' in packages)
        
    
    def test_scan_framework_defaults_to_true(self):
        """ `scan_framework` defaults to `True`, thus appending
          `sys.modules['thruflo.webapp']` to packages.
        """
        
        bootstrapper = self.make_one()
        bootstrapper(packages=[], scan_framework=True)
        packages = bootstrapper.scan.call_args[1]['packages']
        self.assertTrue('thruflo.webapp package' in packages)
        
    
    def test_scan_framework_false(self):
        """ When `scan_framework` is `False`, we don't append
          `sys.modules['thruflo.webapp']` to packages.
        """
        
        bootstrapper = self.make_one()
        bootstrapper(packages=[], scan_framework=False)
        packages = bootstrapper.scan.call_args[1]['packages']
        
        self.assertTrue(not 'thruflo.webapp package' in packages)
        
    
    def test_scan_packages(self):
        """ Calls `self.scan(packages=packages)`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper(scan_framework=False)
        bootstrapper.scan.assert_called_with(packages=[])
        
        bootstrapper = self.make_one()
        bootstrapper(packages=['thruflo.webapp.tests'], scan_framework=False)
        bootstrapper.scan.assert_called_with(
            packages=[sys.modules['thruflo.webapp.tests']]
        )
        
    
    def test_setup_components(self):
        """ Calls `self.setup_components()`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper()
        bootstrapper.setup_components.assert_called_with()
        
    
    def test_returns_registered_settings_and_path_router(self):
        """ Returns `settings, path_router`::
          
              settings = registry.getUtility(IRequirableSettings)
              path_router = registry.getUtility(IPathRouter)
              return settings, path_router
          
        """
        
        from thruflo.webapp.interfaces import IRequirableSettings
        from thruflo.webapp.interfaces import IPathRouter
        
        bootstrapper = self.make_one()
        settings, path_router = bootstrapper()
        
        first_call_args = self.registry.getUtility.call_args_list[0][0]
        self.assertTrue(first_call_args[0] == IRequirableSettings)
        self.assertTrue(settings == 'registered utility')
        
        second_call_args = self.registry.getUtility.call_args_list[1][0]
        self.assertTrue(second_call_args[0] == IPathRouter)
        self.assertTrue(path_router == 'registered utility')
        
    
    

class TestScan(unittest.TestCase):
    """ Test the logic of `Bootstrap.scan`.
    """
    
    def setUp(self):
        from thruflo.webapp import bootstrap
        self.__venusian = bootstrap.venusian
        self.venusian = Mock()
        self.scanner = Mock()
        self.venusian.Scanner.return_value = self.scanner
        bootstrap.venusian = self.venusian
        
    
    def tearDown(self):
        from thruflo.webapp import bootstrap
        bootstrap.venusian = self.__venusian
        
    
    def make_one(self, *args, **kwargs):
        from thruflo.webapp.bootstrap import Bootstrapper
        return Bootstrapper(*args, **kwargs)
        
    
    def test_returns_none_without_packages(self):
        """ Returns `None` unless there are packages to deal with::
        """
        
        bootstrapper = self.make_one()
        self.assertTrue(bootstrapper.scan() is None)
        self.assertTrue(bootstrapper.scan(packages=None) is None)
        self.assertTrue(bootstrapper.scan(packages=[]) is None)
        
    
    def test_settings_passed_to_scanner(self):
        """ If `settings` is not `None`, it's passed to `venusian.Scanner`
          as `settings`.
        """
        
        settings = Mock()
        
        bootstrapper = self.make_one()
        bootstrapper.scan(packages=['a'], settings=settings)
        
        self.venusian.Scanner.assert_called_with(settings=settings)
        
    
    def test_settings_none_uses_self__settings(self):
        """ If `settings` is `None`, which is the default, self._settings
          is passed to `venusian.Scanner` as `settings`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper.scan(packages=['a'], settings=None)
        self.venusian.Scanner.assert_called_with(
            settings=bootstrapper._settings
        )
        
        bootstrapper = self.make_one()
        bootstrapper.scan(packages=['a'])
        self.venusian.Scanner.assert_called_with(
            settings=bootstrapper._settings
        )
        
    
    def test_scanner_scan_called_for_each_package(self):
        """ `scanner.scan(package, ...)` is called for each package.
        """
        
        bootstrapper = self.make_one()
        bootstrapper.scan(packages=['a', 'b', 'c'])
        self.assertTrue(self.scanner.scan.call_args_list[0][0][0] == 'a')
        self.assertTrue(self.scanner.scan.call_args_list[1][0][0] == 'b')
        self.assertTrue(self.scanner.scan.call_args_list[2][0][0] == 'c')
        
    
    def test_categories(self):
        """ `scanner.scan` `categories` default to `['thruflo.webapp']` unless
          `extra_categories` are passed in.
        """
        
        bootstrapper = self.make_one()
        bootstrapper.scan(packages=['a'])
        self.scanner.scan.assert_called_with(
            'a', 
            categories=['thruflo.webapp']
        )
        
        bootstrapper = self.make_one()
        bootstrapper.scan(packages=['a'], extra_categories=None)
        self.scanner.scan.assert_called_with(
            'a', 
            categories=['thruflo.webapp']
        )
        
        bootstrapper = self.make_one()
        bootstrapper.scan(packages=['a'], extra_categories=['b', 'c'])
        self.scanner.scan.assert_called_with(
            'a', 
            categories=['thruflo.webapp', 'b', 'c']
        )
        
    
    def test_returns_scanner(self):
        """ Returns `scanner`.
        """
        
        bootstrapper = self.make_one()
        scanner = bootstrapper.scan(packages=['a'])
        self.assertTrue(scanner == self.scanner)
        
    
    


def _was_registered(m, interface):
    """ Takes a mock and the interface it should have been called with
      as the last argument, iterates through the call_args_list and returns
      `True` if it finds the interface.
      
          >>> m = Mock()
          >>> m1 = m('a', 'IFoo')
          >>> m2 = m('b', 'c', 'd', 'e', 'IBar')
          >>> _was_registered(m, 'IFoo')
          True
          >>> _was_registered(m, 'IBar')
          True
          >>> _was_registered(m, 'IBaz')
          False
      
    """
    
    for item in m.call_args_list:
        if item[0][-1] == interface:
            return True
        
    return False
    

def _was_called_with(m, *args, **kwargs):
    """ Takes a mock and the args and kwargs it should have been
      called with, iterates through the call_args_list and returns
      `True` if they match once.
      
          >>> m = Mock()
          >>> m1 = m('a', foo='bar')
          >>> m2 = m('b', baz='blah')
          >>> _was_called_with(m, 'b', baz='blah')
          True
          >>> _was_called_with(m, 'a', foo='bar')
          True
          >>> _was_called_with(m, 'a')
          False
          >>> _was_called_with(m, baz='blah')
          False
      
    """
    
    for item in m.call_args_list:
        if item[0] == args and item[1] == kwargs:
            return True
        
    return False
    


class TestSetupComponents(unittest.TestCase):
    """ Test the logic of `Bootstrap.scan`.
    """
    
    def setUp(self):
        from thruflo.webapp import bootstrap
        self.__registry = bootstrap.registry
        self.registry = Mock()
        self.registry.registerUtility.return_value = 'registered utility'
        self.registry.registerAdapter.return_value = 'registered adapter'
        bootstrap.registry = self.registry
        
    
    def tearDown(self):
        from thruflo.webapp import bootstrap
        bootstrap.registry = self.__registry
        
    
    def make_one(self, *args, **kwargs):
        from thruflo.webapp.bootstrap import Bootstrapper
        return Bootstrapper(*args, **kwargs)
        
    
    def test_settings_false(self):
        """ If `settings` is `False`, nothing is registered.
        """
        
        from thruflo.webapp.interfaces import IRequirableSettings
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(settings=False)
        
        self.assertTrue(
            not _was_registered(
                self.registry.registerUtility,
                IRequirableSettings
            )
        )
        
    
    def test_settings_none(self):
        """ If `settings` is `None`, call `self._settings` with 
          `self._user_settings` and register `self._settings`.
        """
        
        from thruflo.webapp.interfaces import IRequirableSettings
        
        bootstrapper = self.make_one()
        bootstrapper._settings = Mock()
        bootstrapper.setup_components(settings=None)
        
        bootstrapper._settings.assert_called_with(bootstrapper._user_settings)
        self.assertTrue(
            _was_called_with(
                self.registry.registerUtility,
                bootstrapper._settings,
                IRequirableSettings
            )
        )
        
    
    def test_settings_passed_in(self):
        """ If `settings` is neither `False` nor `None`, it's registered.
        """
        
        from thruflo.webapp.interfaces import IRequirableSettings
        
        bootstrapper = self.make_one()
        settings = Mock()
        bootstrapper.setup_components(settings=settings)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerUtility,
                settings,
                IRequirableSettings
            )
        )
        
    
    def test_path_router_false(self):
        """ If `path_router` is `False`, nothing is registered.
        """
        
        from thruflo.webapp.interfaces import IPathRouter
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(path_router=False)
        
        self.assertTrue(
            not _was_registered(
                self.registry.registerUtility,
                IPathRouter
            )
        )
        
    
    def test_path_router_none(self):
        """ If `path_router` is `None`, call `RegExpPathRouter` with 
          `self._url_mapping` and register the resulting `path_router`.
        """
        
        from thruflo.webapp.interfaces import IPathRouter
        
        from thruflo.webapp import bootstrap
        __RegExpPathRouter = bootstrap.RegExpPathRouter
        RegExpPathRouter = Mock()
        RegExpPathRouter.return_value = 'path router'
        bootstrap.RegExpPathRouter = RegExpPathRouter
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(path_router=None)
        
        RegExpPathRouter.assert_called_with(bootstrapper._url_mapping)
        self.assertTrue(
            _was_called_with(
                self.registry.registerUtility,
                'path router',
                IPathRouter
            )
        )
        
        bootstrap.RegExpPathRouter = __RegExpPathRouter
        
    
    def test_path_router_passed_in(self):
        """ If `path_router` is neither `False` nor `None`, it's registered.
        """
        
        from thruflo.webapp.interfaces import IPathRouter
        
        bootstrapper = self.make_one()
        path_router = Mock()
        bootstrapper.setup_components(path_router=path_router)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerUtility,
                path_router,
                IPathRouter
            )
        )
        
    
    def test_template_renderer_false(self):
        """ If `TemplateRenderer` is `False`, nothing is registered.
        """
        
        from thruflo.webapp.interfaces import ITemplateRenderer
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(TemplateRenderer=False)
        
        self.assertTrue(
            not _was_registered(
                self.registry.registerAdapter,
                ITemplateRenderer
            )
        )
        
    
    def test_template_renderer_none(self):
        """ If `TemplateRenderer` is `None`, register `MakoTemplateRenderer`.
        """
        
        from thruflo.webapp.interfaces import IRequirableSettings
        from thruflo.webapp.interfaces import ITemplateRenderer
        
        from thruflo.webapp import bootstrap
        __MakoTemplateRenderer = bootstrap.MakoTemplateRenderer
        MakoTemplateRenderer = Mock()
        bootstrap.MakoTemplateRenderer = MakoTemplateRenderer
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(TemplateRenderer=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                MakoTemplateRenderer,
                required=[IRequirableSettings],
                provided=ITemplateRenderer
            )
        )
        
        bootstrap.MakoTemplateRenderer = __MakoTemplateRenderer
        
    
    def test_template_renderer_passed_in(self):
        """ If `TemplateRenderer` is neither `False` nor `None`, 
          it's registered.
        """
        
        from thruflo.webapp.interfaces import IRequirableSettings
        from thruflo.webapp.interfaces import ITemplateRenderer
        
        bootstrapper = self.make_one()
        TemplateRenderer = Mock()
        bootstrapper.setup_components(TemplateRenderer=TemplateRenderer)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                TemplateRenderer,
                required=[IRequirableSettings],
                provided=ITemplateRenderer
            )
        )
        
    
    def test_authentication_manager_false(self):
        """ If `AuthenticationManager` is `False`, nothing is registered.
        """
        
        from thruflo.webapp.interfaces import IAuthenticationManager
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(AuthenticationManager=False)
        
        self.assertTrue(
            not _was_registered(
                self.registry.registerAdapter,
                IAuthenticationManager
            )
        )
        
    
    def test_authentication_manager_none(self):
        """ If `AuthenticationManager` is `None`, register 
          `TrivialAuthenticationManager`.
        """
        
        from thruflo.webapp.interfaces import IRequest
        from thruflo.webapp.interfaces import IAuthenticationManager
        
        from thruflo.webapp import bootstrap
        __AuthenticationManager = bootstrap.TrivialAuthenticationManager
        AuthenticationManager = Mock()
        bootstrap.TrivialAuthenticationManager = AuthenticationManager
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(TemplateRenderer=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                AuthenticationManager,
                required=[IRequest],
                provided=IAuthenticationManager
            )
        )
        
        bootstrap.TrivialAuthenticationManager = __AuthenticationManager
        
    
    def test_authentication_manager_passed_in(self):
        """ If `AuthenticationManager` is neither `False` nor `None`, 
          it's registered.
        """
        
        from thruflo.webapp.interfaces import IRequest
        from thruflo.webapp.interfaces import IAuthenticationManager
        
        bootstrapper = self.make_one()
        AuthenticationManager = Mock()
        bootstrapper.setup_components(
            AuthenticationManager=AuthenticationManager
        )
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                AuthenticationManager,
                required=[IRequest],
                provided=IAuthenticationManager
            )
        )
        
    
    def test_static_url_generator_false(self):
        """ If `StaticURLGenerator` is `False`, nothing is registered.
        """
        
        from thruflo.webapp.interfaces import IStaticURLGenerator
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(StaticURLGenerator=False)
        
        self.assertTrue(
            not _was_registered(
                self.registry.registerAdapter,
                IStaticURLGenerator
            )
        )
        
    
    def test_static_url_generator_none(self):
        """ If `StaticURLGenerator` is `None`, register 
          `MemoryCachedStaticURLGenerator`.
        """
        
        from thruflo.webapp.interfaces import IRequest
        from thruflo.webapp.interfaces import IRequirableSettings
        from thruflo.webapp.interfaces import IStaticURLGenerator
        
        from thruflo.webapp import bootstrap
        __StaticURLGenerator = bootstrap.MemoryCachedStaticURLGenerator
        StaticURLGenerator = Mock()
        bootstrap.MemoryCachedStaticURLGenerator = StaticURLGenerator
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(StaticURLGenerator=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                StaticURLGenerator, 
                required=[IRequest, IRequirableSettings],
                provided=IStaticURLGenerator
            )
        )
        
        bootstrap.MemoryCachedStaticURLGenerator = __StaticURLGenerator
        
    
    def test_static_url_generator_passed_in(self):
        """ If `StaticURLGenerator` is neither `False` nor `None`, 
          it's registered.
        """
        
        from thruflo.webapp.interfaces import IRequest
        from thruflo.webapp.interfaces import IRequirableSettings
        from thruflo.webapp.interfaces import IStaticURLGenerator
        
        bootstrapper = self.make_one()
        StaticURLGenerator = Mock()
        bootstrapper.setup_components(StaticURLGenerator=StaticURLGenerator)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                StaticURLGenerator, 
                required=[IRequest, IRequirableSettings],
                provided=IStaticURLGenerator
            )
        )
        
    
    def test_secure_cookie_wrapper_false(self):
        """ If `SecureCookieWrapper` is `False`, nothing is registered.
        """
        
        from thruflo.webapp.interfaces import ISecureCookieWrapper
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(SecureCookieWrapper=False)
        
        self.assertTrue(
            not _was_registered(
                self.registry.registerAdapter,
                ISecureCookieWrapper
            )
        )
        
    
    def test_secure_cookie_wrapper_none(self):
        """ If `SecureCookieWrapper` is `None`, register 
          `SignedSecureCookieWrapper`.
        """
        
        from thruflo.webapp.interfaces import IRequest, IResponse
        from thruflo.webapp.interfaces import IRequirableSettings
        from thruflo.webapp.interfaces import ISecureCookieWrapper
        
        from thruflo.webapp import bootstrap
        __SecureCookieWrapper = bootstrap.SignedSecureCookieWrapper
        SecureCookieWrapper = Mock()
        bootstrap.SignedSecureCookieWrapper = SecureCookieWrapper
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(SecureCookieWrapper=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                SecureCookieWrapper, 
                required=[IRequest, IResponse, IRequirableSettings],
                provided=ISecureCookieWrapper
            )
        )
        
        bootstrap.MemoryCachedSecureCookieWrapper = __SecureCookieWrapper
        
    
    def test_secure_cookie_wrapper_passed_in(self):
        """ If `SecureCookieWrapper` is neither `False` nor `None`, 
          it's registered.
        """
        
        from thruflo.webapp.interfaces import IRequest, IResponse
        from thruflo.webapp.interfaces import IRequirableSettings
        from thruflo.webapp.interfaces import ISecureCookieWrapper
        
        bootstrapper = self.make_one()
        SecureCookieWrapper = Mock()
        bootstrapper.setup_components(SecureCookieWrapper=SecureCookieWrapper)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                SecureCookieWrapper, 
                required=[IRequest, IResponse, IRequirableSettings],
                provided=ISecureCookieWrapper
            )
        )
        
    
    def test_method_selector_false(self):
        """ If `MethodSelector` is `False`, nothing is registered.
        """
        
        from thruflo.webapp.interfaces import IMethodSelector
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(MethodSelector=False)
        
        self.assertTrue(
            not _was_registered(
                self.registry.registerAdapter,
                IMethodSelector
            )
        )
        
    
    def test_method_selector_none(self):
        """ If `MethodSelector` is `None`, register 
          `ExposedMethodSelector`.
        """
        
        from thruflo.webapp.interfaces import IRequestHandler
        from thruflo.webapp.interfaces import IMethodSelector
        
        from thruflo.webapp import bootstrap
        __MethodSelector = bootstrap.ExposedMethodSelector
        MethodSelector = Mock()
        bootstrap.ExposedMethodSelector = MethodSelector
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(MethodSelector=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                MethodSelector, 
                required=[IRequestHandler],
                provided=IMethodSelector
            )
        )
        
        bootstrap.ExposedMethodSelector = __MethodSelector
        
    
    def test_method_selector_passed_in(self):
        """ If `MethodSelector` is neither `False` nor `None`, 
          it's registered.
        """
        
        from thruflo.webapp.interfaces import IRequestHandler
        from thruflo.webapp.interfaces import IMethodSelector
        
        bootstrapper = self.make_one()
        MethodSelector = Mock()
        bootstrapper.setup_components(MethodSelector=MethodSelector)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                MethodSelector, 
                required=[IRequestHandler],
                provided=IMethodSelector
            )
        )
        
    
    def test_response_normaliser_false(self):
        """ If `ResponseNormaliser` is `False`, nothing is registered.
        """
        
        from thruflo.webapp.interfaces import IResponseNormaliser
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(ResponseNormaliser=False)
        
        self.assertTrue(
            not _was_registered(
                self.registry.registerAdapter,
                IResponseNormaliser
            )
        )
        
    
    def test_response_normaliser_none(self):
        """ If `ResponseNormaliser` is `None`, register 
          `DefaultToJSONResponseNormaliser`.
        """
        
        from thruflo.webapp.interfaces import IResponse
        from thruflo.webapp.interfaces import IResponseNormaliser
        
        from thruflo.webapp import bootstrap
        __ResponseNormaliser = bootstrap.DefaultToJSONResponseNormaliser
        ResponseNormaliser = Mock()
        bootstrap.DefaultToJSONResponseNormaliser = ResponseNormaliser
        
        bootstrapper = self.make_one()
        bootstrapper.setup_components(ResponseNormaliser=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                ResponseNormaliser, 
                required=[IResponse],
                provided=IResponseNormaliser
            )
        )
        
        bootstrap.DefaultToJSONResponseNormaliser = __ResponseNormaliser
        
    
    def test_response_normaliser_passed_in(self):
        """ If `ResponseNormaliser` is neither `False` nor `None`, 
          it's registered.
        """
        
        from thruflo.webapp.interfaces import IResponse
        from thruflo.webapp.interfaces import IResponseNormaliser
        
        bootstrapper = self.make_one()
        ResponseNormaliser = Mock()
        bootstrapper.setup_components(ResponseNormaliser=ResponseNormaliser)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                ResponseNormaliser, 
                required=[IResponse],
                provided=IResponseNormaliser
            )
        )
        
    
    



