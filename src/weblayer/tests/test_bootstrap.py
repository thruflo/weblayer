#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for `weblayer.bootstrap`.
"""

import unittest
from mock import Mock

class TestInitBootstrapper(unittest.TestCase):
    """ Test the logic of `Bootstrap.__init__`.
    """
    
    def make_one(self, *args, **kwargs):
        from weblayer.bootstrap import Bootstrapper
        return Bootstrapper(*args, **kwargs)
        
    
    def test_init_settings(self):
        """ `settings` is available as `self._user_settings`.
        """
        
        settings = Mock()
        bootstrapper = self.make_one(settings=settings)
        self.assertTrue(bootstrapper._user_settings == settings)
        
    
    def test_init_url_map(self):
        """ `url_mapping` is available as `self._url_mapping`.
        """
        
        url_mapping = Mock()
        bootstrapper = self.make_one(url_mapping=url_mapping)
        self.assertTrue(bootstrapper._url_mapping == url_mapping)
        
    
    

class TestCallBootstrapper(unittest.TestCase):
    """ Test the logic of `Bootstrap.__call__`.
    """
    
    def setUp(self):
        from weblayer import bootstrap
        self.__registry = bootstrap.registry
        self.registry = Mock()
        self.registry.getUtility.return_value = 'registered utility'
        bootstrap.registry = self.registry
        
    
    def tearDown(self):
        from weblayer import bootstrap
        bootstrap.registry = self.__registry
        
    
    def make_one(self, *args, **kwargs):
        from weblayer.bootstrap import Bootstrapper
        bootstrapper = Bootstrapper(*args, **kwargs)
        bootstrapper.require_settings = Mock()
        bootstrapper.require_settings.return_value = 'required settings'
        bootstrapper.register_components = Mock()
        return bootstrapper
        
    
    def test_register_components_settings_kwarg(self):
        """ Calls `self.register_components(settings={'a': 'b'})`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper(settings={'a': 'b'})
        bootstrapper.register_components.assert_called_with(
            settings={'a': 'b'}
        )
        
    
    def test_require_settings_register_components(self):
        """ Calls `self.register_components(settings=settings)`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper(require_settings=True)
        bootstrapper.register_components.assert_called_with(
            settings='required settings'
        )
        
    
    def test_require_settings_by_default(self):
        """ Calls `self.register_components(settings=settings)` by default.
        """
        
        bootstrapper = self.make_one()
        bootstrapper()
        bootstrapper.register_components.assert_called_with(settings='required settings')
        
    
    def test_require_settings_false_register_components(self):
        """ Calls `self.register_components(settings=None)`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper(require_settings=False)
        bootstrapper.register_components.assert_called_with(
            settings=None
        )
        
    
    def test_register_components_path_router_kwarg(self):
        """ Calls `self.register_components(path_router='path router')`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper(path_router='path router')
        bootstrapper.register_components.assert_called_with(
            settings='required settings', 
            path_router='path router'
        )
        
    
    def test_require_settings_packages(self):
        """ Passes `packages` through to `self.require_settings`, defaulting
          to `None`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper()
        args = bootstrapper.require_settings.call_args
        packages = args[1]['packages']
        self.assertTrue(packages is None)
        
        bootstrapper(packages=['foo'])
        args = bootstrapper.require_settings.call_args
        packages = args[1]['packages']
        self.assertTrue(packages == ['foo'])
        
    
    def test_require_settings_scan_framework(self):
        """ Passes `scan_framework` through to `self.require_settings`,
          defaulting to `True`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper()
        args = bootstrapper.require_settings.call_args
        scan_framework = args[1]['scan_framework']
        self.assertTrue(scan_framework is True)
        
        bootstrapper(scan_framework=False)
        args = bootstrapper.require_settings.call_args
        scan_framework = args[1]['scan_framework']
        self.assertTrue(scan_framework is False)
        
    
    def test_require_settings_extra_categories(self):
        """ Passes `extra_categories` through to `self.require_settings`,
          defaulting to `None`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper()
        args = bootstrapper.require_settings.call_args
        extra_categories = args[1]['extra_categories']
        self.assertTrue(extra_categories is None)
        
        bootstrapper(extra_categories=['a', 'b', 'c'])
        args = bootstrapper.require_settings.call_args
        extra_categories = args[1]['extra_categories']
        self.assertTrue(extra_categories == ['a', 'b', 'c'])
        
    
    def test_returns_registered_settings_and_path_router(self):
        """ Returns `settings, path_router`.
        """
        
        from weblayer.interfaces import ISettings
        from weblayer.interfaces import IPathRouter
        
        bootstrapper = self.make_one()
        settings, path_router = bootstrapper()
        
        first_call_args = self.registry.getUtility.call_args_list[0][0]
        self.assertTrue(first_call_args[0] == ISettings)
        self.assertTrue(settings == 'registered utility')
        
        second_call_args = self.registry.getUtility.call_args_list[1][0]
        self.assertTrue(second_call_args[0] == IPathRouter)
        self.assertTrue(path_router == 'registered utility')
        
    
    

class TestBootstrapperRequireSettings(unittest.TestCase):
    """ Test the logic of `bootstrapper.require_settings`.
    """
    
    def setUp(self):
        from weblayer import bootstrap
        self.__sys = bootstrap.sys
        self.__RequirableSettings = bootstrap.RequirableSettings
        self.sys = Mock()
        self.sys.modules = {
            'weblayer': 'weblayer package', 
            'a': 'a package', 
            'b': 'b package'
        }
        self.RequirableSettings = Mock()
        self.RequirableSettings.return_value = 'requirable settings'
        bootstrap.sys = self.sys
        bootstrap.RequirableSettings = self.RequirableSettings
        
    
    def tearDown(self):
        from weblayer import bootstrap
        bootstrap.sys = self.__sys
        bootstrap.RequirableSettings = self.__RequirableSettings
        
    
    def make_one(self, *args, **kwargs):
        from weblayer.bootstrap import Bootstrapper
        return Bootstrapper(*args, **kwargs)
        
    
    def test_packages(self):
        """ If `packages` is not `None`, which it defaults to`, passes each
          item in `packages` through to `RequirableSettings`,
          preceeded by 'weblayer' if scan_framework is True, which is
          the default.
        """
        
        bootstrapper = self.make_one()
        bootstrapper.require_settings(packages=None, scan_framework=False)
        args = self.RequirableSettings.call_args
        packages = args[1]['packages']
        self.assertTrue(packages == [])
        
        bootstrapper = self.make_one()
        bootstrapper.require_settings(scan_framework=False)
        args = self.RequirableSettings.call_args
        packages = args[1]['packages']
        self.assertTrue(packages == [])
        
        bootstrapper = self.make_one()
        bootstrapper.require_settings()
        args = self.RequirableSettings.call_args
        packages = args[1]['packages']
        self.assertTrue(packages == ['weblayer package'])
        
        bootstrapper = self.make_one()
        bootstrapper.require_settings(packages=['a', 'b'])
        args = self.RequirableSettings.call_args
        packages = args[1]['packages']
        
        self.assertTrue(
            packages == ['weblayer package', 'a package', 'b package']
        )
        
    
    def test_extra_categories(self):
        """ `extra_categories` is passed to `RequirableSettings`
          defaulting to `None`.
        """
        
        bootstrapper = self.make_one()
        bootstrapper.require_settings(extra_categories=None)
        args = self.RequirableSettings.call_args
        extra_categories = args[1]['extra_categories']
        self.assertTrue(extra_categories is None)
        
        bootstrapper = self.make_one()
        bootstrapper.require_settings()
        args = self.RequirableSettings.call_args
        extra_categories = args[1]['extra_categories']
        self.assertTrue(extra_categories is None)
        
        bootstrapper = self.make_one()
        bootstrapper.require_settings(extra_categories=['a', 'b', 'c'])
        args = self.RequirableSettings.call_args
        extra_categories = args[1]['extra_categories']
        self.assertTrue(extra_categories == ['a', 'b', 'c'])
        
    
    def test_returns_settings(self):
        """ Returns `settings`.
        """
        
        bootstrapper = self.make_one()
        settings = bootstrapper.require_settings()
        self.assertTrue(settings == 'requirable settings')
        
    
    


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
    


class TestBootstrapperRegisterComponents(unittest.TestCase):
    """ Test the logic of `bootstrapper.register_components`.
    """
    
    def setUp(self):
        from weblayer import bootstrap
        self.__registry = bootstrap.registry
        self.registry = Mock()
        self.registry.registerUtility.return_value = 'registered utility'
        self.registry.registerAdapter.return_value = 'registered adapter'
        bootstrap.registry = self.registry
        
    
    def tearDown(self):
        from weblayer import bootstrap
        bootstrap.registry = self.__registry
        
    
    def make_one(self, *args, **kwargs):
        from weblayer.bootstrap import Bootstrapper
        return Bootstrapper(*args, **kwargs)
        
    
    def test_settings_false(self):
        """ If `settings` is `False`, nothing is registered.
        """
        
        from weblayer.interfaces import ISettings
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(settings=False)
        
        self.assertTrue(
            not _was_registered(
                self.registry.registerUtility,
                ISettings
            )
        )
        
    
    def test_settings_none(self):
        """ If `settings` is `None`, init `RequirableSettings`,
          call with `self._user_settings` and register `self._settings`.
        """
        
        from weblayer.interfaces import ISettings
        
        from weblayer import bootstrap
        __RequirableSettings = bootstrap.RequirableSettings
        RequirableSettings = Mock()
        requirable_settings = Mock()
        RequirableSettings.return_value = requirable_settings
        bootstrap.RequirableSettings = RequirableSettings
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(settings=None)
        
        RequirableSettings.assert_called_with()
        requirable_settings.assert_called_with(bootstrapper._user_settings)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerUtility,
                requirable_settings,
                ISettings
            )
        )
        
    
    def test_settings_default_to_none(self):
        """ Init `RequirableSettings`, call with 
          `self._user_settings` and register `self._settings`.
        """
        
        from weblayer.interfaces import ISettings
        
        from weblayer import bootstrap
        __RequirableSettings = bootstrap.RequirableSettings
        RequirableSettings = Mock()
        requirable_settings = Mock()
        RequirableSettings.return_value = requirable_settings
        bootstrap.RequirableSettings = RequirableSettings
        
        bootstrapper = self.make_one()
        bootstrapper.register_components()
        
        RequirableSettings.assert_called_with()
        requirable_settings.assert_called_with(bootstrapper._user_settings)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerUtility,
                requirable_settings,
                ISettings
            )
        )
        
    
    def test_settings_passed_in(self):
        """ If `settings` is neither `False` nor `None`, it's called
          with `self._user_settings` and registered.
        """
        
        from weblayer.interfaces import ISettings
        
        bootstrapper = self.make_one()
        settings = Mock()
        bootstrapper.register_components(settings=settings)
        
        settings.assert_called_with(bootstrapper._user_settings)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerUtility,
                settings,
                ISettings
            )
        )
        
    
    def test_path_router_false(self):
        """ If `path_router` is `False`, nothing is registered.
        """
        
        from weblayer.interfaces import IPathRouter
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(path_router=False)
        
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
        
        from weblayer.interfaces import IPathRouter
        
        from weblayer import bootstrap
        __RegExpPathRouter = bootstrap.RegExpPathRouter
        RegExpPathRouter = Mock()
        RegExpPathRouter.return_value = 'path router'
        bootstrap.RegExpPathRouter = RegExpPathRouter
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(path_router=None)
        
        RegExpPathRouter.assert_called_with(bootstrapper._url_mapping)
        self.assertTrue(
            _was_called_with(
                self.registry.registerUtility,
                'path router',
                IPathRouter
            )
        )
        
        bootstrap.RegExpPathRouter = __RegExpPathRouter
        
    
    def test_path_router_defaults_to_none(self):
        """ Call `RegExpPathRouter` with `self._url_mapping` and register
          the resulting `path_router`.
        """
        
        from weblayer.interfaces import IPathRouter
        
        from weblayer import bootstrap
        __RegExpPathRouter = bootstrap.RegExpPathRouter
        RegExpPathRouter = Mock()
        RegExpPathRouter.return_value = 'path router'
        bootstrap.RegExpPathRouter = RegExpPathRouter
        
        bootstrapper = self.make_one()
        bootstrapper.register_components()
        
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
        
        from weblayer.interfaces import IPathRouter
        
        bootstrapper = self.make_one()
        path_router = Mock()
        bootstrapper.register_components(path_router=path_router)
        
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
        
        from weblayer.interfaces import ITemplateRenderer
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(TemplateRenderer=False)
        
        self.assertTrue(
            not _was_registered(
                self.registry.registerAdapter,
                ITemplateRenderer
            )
        )
        
    
    def test_template_renderer_none(self):
        """ If `TemplateRenderer` is `None`, register `MakoTemplateRenderer`.
        """
        
        from weblayer.interfaces import ISettings
        from weblayer.interfaces import ITemplateRenderer
        
        from weblayer import bootstrap
        __MakoTemplateRenderer = bootstrap.MakoTemplateRenderer
        MakoTemplateRenderer = Mock()
        bootstrap.MakoTemplateRenderer = MakoTemplateRenderer
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(TemplateRenderer=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                MakoTemplateRenderer,
                required=[ISettings],
                provided=ITemplateRenderer
            )
        )
        
        bootstrap.MakoTemplateRenderer = __MakoTemplateRenderer
        
    
    def test_template_renderer_defaults_to_none(self):
        """ Register `MakoTemplateRenderer`.
        """
        
        from weblayer.interfaces import ISettings
        from weblayer.interfaces import ITemplateRenderer
        
        from weblayer import bootstrap
        __MakoTemplateRenderer = bootstrap.MakoTemplateRenderer
        MakoTemplateRenderer = Mock()
        bootstrap.MakoTemplateRenderer = MakoTemplateRenderer
        
        bootstrapper = self.make_one()
        bootstrapper.register_components()
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                MakoTemplateRenderer,
                required=[ISettings],
                provided=ITemplateRenderer
            )
        )
        
        bootstrap.MakoTemplateRenderer = __MakoTemplateRenderer
        
    
    def test_template_renderer_passed_in(self):
        """ If `TemplateRenderer` is neither `False` nor `None`, 
          it's registered.
        """
        
        from weblayer.interfaces import ISettings
        from weblayer.interfaces import ITemplateRenderer
        
        bootstrapper = self.make_one()
        TemplateRenderer = Mock()
        bootstrapper.register_components(TemplateRenderer=TemplateRenderer)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                TemplateRenderer,
                required=[ISettings],
                provided=ITemplateRenderer
            )
        )
        
    
    def test_authentication_manager_false(self):
        """ If `AuthenticationManager` is `False`, nothing is registered.
        """
        
        from weblayer.interfaces import IAuthenticationManager
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(AuthenticationManager=False)
        
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
        
        from weblayer.interfaces import IRequest
        from weblayer.interfaces import IAuthenticationManager
        
        from weblayer import bootstrap
        __AuthenticationManager = bootstrap.TrivialAuthenticationManager
        AuthenticationManager = Mock()
        bootstrap.TrivialAuthenticationManager = AuthenticationManager
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(AuthenticationManager=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                AuthenticationManager,
                required=[IRequest],
                provided=IAuthenticationManager
            )
        )
        
        bootstrap.TrivialAuthenticationManager = __AuthenticationManager
        
    
    def test_authentication_manager_defaults_to_none(self):
        """ Register `TrivialAuthenticationManager`.
        """
        
        from weblayer.interfaces import IRequest
        from weblayer.interfaces import IAuthenticationManager
        
        from weblayer import bootstrap
        __AuthenticationManager = bootstrap.TrivialAuthenticationManager
        AuthenticationManager = Mock()
        bootstrap.TrivialAuthenticationManager = AuthenticationManager
        
        bootstrapper = self.make_one()
        bootstrapper.register_components()
        
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
        
        from weblayer.interfaces import IRequest
        from weblayer.interfaces import IAuthenticationManager
        
        bootstrapper = self.make_one()
        AuthenticationManager = Mock()
        bootstrapper.register_components(
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
        
        from weblayer.interfaces import IStaticURLGenerator
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(StaticURLGenerator=False)
        
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
        
        from weblayer.interfaces import IRequest
        from weblayer.interfaces import ISettings
        from weblayer.interfaces import IStaticURLGenerator
        
        from weblayer import bootstrap
        __StaticURLGenerator = bootstrap.MemoryCachedStaticURLGenerator
        StaticURLGenerator = Mock()
        bootstrap.MemoryCachedStaticURLGenerator = StaticURLGenerator
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(StaticURLGenerator=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                StaticURLGenerator, 
                required=[IRequest, ISettings],
                provided=IStaticURLGenerator
            )
        )
        
        bootstrap.MemoryCachedStaticURLGenerator = __StaticURLGenerator
        
    
    def test_static_url_generator_defaults_none(self):
        """ Register `MemoryCachedStaticURLGenerator`.
        """
        
        from weblayer.interfaces import IRequest
        from weblayer.interfaces import ISettings
        from weblayer.interfaces import IStaticURLGenerator
        
        from weblayer import bootstrap
        __StaticURLGenerator = bootstrap.MemoryCachedStaticURLGenerator
        StaticURLGenerator = Mock()
        bootstrap.MemoryCachedStaticURLGenerator = StaticURLGenerator
        
        bootstrapper = self.make_one()
        bootstrapper.register_components()
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                StaticURLGenerator, 
                required=[IRequest, ISettings],
                provided=IStaticURLGenerator
            )
        )
        
        bootstrap.MemoryCachedStaticURLGenerator = __StaticURLGenerator
        
    
    def test_static_url_generator_passed_in(self):
        """ If `StaticURLGenerator` is neither `False` nor `None`, 
          it's registered.
        """
        
        from weblayer.interfaces import IRequest
        from weblayer.interfaces import ISettings
        from weblayer.interfaces import IStaticURLGenerator
        
        bootstrapper = self.make_one()
        StaticURLGenerator = Mock()
        bootstrapper.register_components(StaticURLGenerator=StaticURLGenerator)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                StaticURLGenerator, 
                required=[IRequest, ISettings],
                provided=IStaticURLGenerator
            )
        )
        
    
    def test_secure_cookie_wrapper_false(self):
        """ If `SecureCookieWrapper` is `False`, nothing is registered.
        """
        
        from weblayer.interfaces import ISecureCookieWrapper
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(SecureCookieWrapper=False)
        
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
        
        from weblayer.interfaces import IRequest, IResponse
        from weblayer.interfaces import ISettings
        from weblayer.interfaces import ISecureCookieWrapper
        
        from weblayer import bootstrap
        __SecureCookieWrapper = bootstrap.SignedSecureCookieWrapper
        SecureCookieWrapper = Mock()
        bootstrap.SignedSecureCookieWrapper = SecureCookieWrapper
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(SecureCookieWrapper=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                SecureCookieWrapper, 
                required=[IRequest, IResponse, ISettings],
                provided=ISecureCookieWrapper
            )
        )
        
        bootstrap.MemoryCachedSecureCookieWrapper = __SecureCookieWrapper
        
    
    def test_secure_cookie_wrapper_defaults_none(self):
        """ Register `SignedSecureCookieWrapper`.
        """
        
        from weblayer.interfaces import IRequest, IResponse
        from weblayer.interfaces import ISettings
        from weblayer.interfaces import ISecureCookieWrapper
        
        from weblayer import bootstrap
        __SecureCookieWrapper = bootstrap.SignedSecureCookieWrapper
        SecureCookieWrapper = Mock()
        bootstrap.SignedSecureCookieWrapper = SecureCookieWrapper
        
        bootstrapper = self.make_one()
        bootstrapper.register_components()
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                SecureCookieWrapper, 
                required=[IRequest, IResponse, ISettings],
                provided=ISecureCookieWrapper
            )
        )
        
        bootstrap.MemoryCachedSecureCookieWrapper = __SecureCookieWrapper
        
    
    def test_secure_cookie_wrapper_passed_in(self):
        """ If `SecureCookieWrapper` is neither `False` nor `None`, 
          it's registered.
        """
        
        from weblayer.interfaces import IRequest, IResponse
        from weblayer.interfaces import ISettings
        from weblayer.interfaces import ISecureCookieWrapper
        
        bootstrapper = self.make_one()
        SecureCookieWrapper = Mock()
        bootstrapper.register_components(SecureCookieWrapper=SecureCookieWrapper)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                SecureCookieWrapper, 
                required=[IRequest, IResponse, ISettings],
                provided=ISecureCookieWrapper
            )
        )
        
    
    def test_method_selector_false(self):
        """ If `MethodSelector` is `False`, nothing is registered.
        """
        
        from weblayer.interfaces import IMethodSelector
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(MethodSelector=False)
        
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
        
        from weblayer.interfaces import IRequestHandler
        from weblayer.interfaces import IMethodSelector
        
        from weblayer import bootstrap
        __MethodSelector = bootstrap.ExposedMethodSelector
        MethodSelector = Mock()
        bootstrap.ExposedMethodSelector = MethodSelector
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(MethodSelector=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                MethodSelector, 
                required=[IRequestHandler],
                provided=IMethodSelector
            )
        )
        
        bootstrap.ExposedMethodSelector = __MethodSelector
        
    
    def test_method_selector_defaults_to_none(self):
        """ Register `ExposedMethodSelector`.
        """
        
        from weblayer.interfaces import IRequestHandler
        from weblayer.interfaces import IMethodSelector
        
        from weblayer import bootstrap
        __MethodSelector = bootstrap.ExposedMethodSelector
        MethodSelector = Mock()
        bootstrap.ExposedMethodSelector = MethodSelector
        
        bootstrapper = self.make_one()
        bootstrapper.register_components()
        
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
        
        from weblayer.interfaces import IRequestHandler
        from weblayer.interfaces import IMethodSelector
        
        bootstrapper = self.make_one()
        MethodSelector = Mock()
        bootstrapper.register_components(MethodSelector=MethodSelector)
        
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
        
        from weblayer.interfaces import IResponseNormaliser
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(ResponseNormaliser=False)
        
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
        
        from weblayer.interfaces import IResponse
        from weblayer.interfaces import IResponseNormaliser
        
        from weblayer import bootstrap
        __ResponseNormaliser = bootstrap.DefaultToJSONResponseNormaliser
        ResponseNormaliser = Mock()
        bootstrap.DefaultToJSONResponseNormaliser = ResponseNormaliser
        
        bootstrapper = self.make_one()
        bootstrapper.register_components(ResponseNormaliser=None)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                ResponseNormaliser, 
                required=[IResponse],
                provided=IResponseNormaliser
            )
        )
        
        bootstrap.DefaultToJSONResponseNormaliser = __ResponseNormaliser
        
    
    def test_response_normaliser_defaults_to_none(self):
        """ Register `DefaultToJSONResponseNormaliser`.
        """
        
        from weblayer.interfaces import IResponse
        from weblayer.interfaces import IResponseNormaliser
        
        from weblayer import bootstrap
        __ResponseNormaliser = bootstrap.DefaultToJSONResponseNormaliser
        ResponseNormaliser = Mock()
        bootstrap.DefaultToJSONResponseNormaliser = ResponseNormaliser
        
        bootstrapper = self.make_one()
        bootstrapper.register_components()
        
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
        
        from weblayer.interfaces import IResponse
        from weblayer.interfaces import IResponseNormaliser
        
        bootstrapper = self.make_one()
        ResponseNormaliser = Mock()
        bootstrapper.register_components(ResponseNormaliser=ResponseNormaliser)
        
        self.assertTrue(
            _was_called_with(
                self.registry.registerAdapter,
                ResponseNormaliser, 
                required=[IResponse],
                provided=IResponseNormaliser
            )
        )
        
    
    

