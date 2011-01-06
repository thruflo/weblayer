#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit and integration tests for `weblayer.settings`.
"""

import unittest
from mock import Mock

class TestInit(unittest.TestCase):
    """ Test the logic of `RequirableSettings.__init__`.
    """
    
    def setUp(self):
        from weblayer import settings
        self.__venusian = settings.venusian
        self.venusian = Mock()
        self.scanner = Mock()
        self.venusian.Scanner.return_value = self.scanner
        settings.venusian = self.venusian
        
    
    def tearDown(self):
        from weblayer import settings
        settings.venusian = self.__venusian
        
    
    def make_one(self, *args, **kwargs):
        from weblayer.settings import RequirableSettings
        return RequirableSettings(*args, **kwargs)
        
    
    def test_required_settings_and_items_are_empty_dicts(self):
        """ `self.__required_settings__` and `self._items` are empty dicts.
        """
        
        settings = self.make_one()
        self.assertTrue(settings.__required_settings__ == {})
        self.assertTrue(settings._items == {})
        
    
    def test_scanner_init_with_settings_if_packages(self):
        """ If `packages` are provided, which is not the case by default,
          inits a `venusian.Scanner` with `settings=self`
        """
        
        settings = self.make_one()
        self.assertTrue(not self.venusian.Scanner.called)
        
        settings = self.make_one(packages=[])
        self.assertTrue(not self.venusian.Scanner.called)
        
        settings = self.make_one(packages=['a', 'b'])
        self.venusian.Scanner.assert_called_with(settings=settings)
        
    
    def test_scan_each_package(self):
        """ If a list of `packages` is provided, scans them in turn.
        """
        
        settings = self.make_one(packages=['a'])
        args = self.scanner.scan.call_args[0]
        self.assertTrue(args[0] == 'a')
        
        settings = self.make_one(packages=['b', 'c', 'd'])
        args = self.scanner.scan.call_args[0]
        self.assertTrue(args[0] == 'd')
        
        self.assertTrue(len(self.scanner.scan.call_args_list) == 4)
        
    
    def test_categories(self):
        """ `categories` defaults to `[_CATEGORY]` unless `extra_categories`
          are provided.
        """
        
        from weblayer.settings import _CATEGORY
        
        settings = self.make_one(packages=['a'])
        kwargs = self.scanner.scan.call_args[1]
        self.assertTrue(kwargs['categories'] == [_CATEGORY])
        
        settings = self.make_one(packages=['a'], extra_categories=None)
        kwargs = self.scanner.scan.call_args[1]
        self.assertTrue(kwargs['categories'] == [_CATEGORY])
        
        settings = self.make_one(packages=['a'], extra_categories=['b', 'c'])
        kwargs = self.scanner.scan.call_args[1]
        self.assertTrue(kwargs['categories'] == [_CATEGORY, 'b', 'c'])
        
    
    

class TestIntegration(unittest.TestCase):
    """ Test requiring and overriding settings.
    """
    
    def setUp(self):
        self.required_items = {
            'test_module': 'some value',
            'test_function': 'some value',
            'test_method': 'some value'
        }
        
    
    def make_one(self, packages):
        from weblayer.settings import RequirableSettings
        return RequirableSettings(
            packages=packages,
            extra_categories=['weblayer.tests']
        )
        
    
    def test_required_items(self):
        """ This is our control: calling `settings` with `self.required_items`
          should be fine.
        """
        
        from weblayer.tests.fixtures import require
        settings = self.make_one([require])
        
        settings(self.required_items)
        self.assertTrue(settings['test_module'] == 'some value')
        self.assertTrue(settings['test_function'] == 'some value')
        self.assertTrue(settings['test_method'] == 'some value')
        
    
    def test_module(self):
        """ `test_module` should be required.
        """
        
        from weblayer.tests.fixtures import require
        settings = self.make_one([require])
        
        items = self.required_items.copy()
        del items['test_module']
        self.assertRaises(
            KeyError,
            settings,
            items
        )
        
    
    def test_function(self):
        """ `test_function` should be required.
        """
        
        from weblayer.tests.fixtures import require
        settings = self.make_one([require])
        
        items = self.required_items.copy()
        del items['test_function']
        self.assertRaises(
            KeyError,
            settings,
            items
        )
        
    
    def test_method(self):
        """ `test_method` should be required.
        """
        
        from weblayer.tests.fixtures import require
        settings = self.make_one([require])
        
        items = self.required_items.copy()
        del items['test_method']
        self.assertRaises(
            KeyError,
            settings,
            items
        )
        
    
    def test_override(self):
        """ Test the overrides.
        """
        
        from weblayer.tests.fixtures import require, override
        
        settings = self.make_one([require, override])
        settings(self.required_items)
        self.assertTrue(settings['test_override_function'] == 'something else')
        
    
    

class TestDoubleImport(unittest.TestCase):
    """ See http://bit.ly/dIKcX9, specifically the bit that says
      
          This has the effect that double-registrations will never 
          be performed.
      
      `weblayer.settings` is our equivalent of that article's 
      `config.py`, `.fixtures.require` `app.py` and `.fixtures.double_import`
      is like `app2.py`.
    """
    
    def make_one(self, packages):
        from weblayer.settings import RequirableSettings
        return RequirableSettings(
            packages=packages,
            extra_categories=['weblayer.tests']
        )
        
    
    def test__require_called_once(self):
        """ `app2` imports `app`, which means the `require_setting`
          above would be run twice if we called `_require` on import.
          
        """
        
        from weblayer.settings import RequirableSettings
        __require = RequirableSettings._require
        _require = Mock()
        RequirableSettings._require = _require
        
        from weblayer.tests.fixtures import require
        from weblayer.tests.fixtures import double_import
        
        settings = self.make_one(packages=[require, double_import])
        
        self.assertTrue(_require.call_args_list == [((
                        'test_module',
                    ), {
                        'default': None, 
                        'help': u''
                    }
                ), ((
                        'test_function',
                    ), {
                        'default': None, 
                        'help': u''
                    }
                ), ((
                        'test_method',
                    ), {
                        'default': None, 
                        'help': u''
                    }
                )
            ]
        )
        
        RequirableSettings._require = __require
        
    
    

