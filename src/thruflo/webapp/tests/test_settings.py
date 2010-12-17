#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit and integration tests for `thruflo.webapp.settings`.
"""

import venusian
import unittest
from mock import Mock

from zope.interface import implements

from thruflo.webapp.settings import RequirableSettings
from thruflo.webapp.settings import require, require_setting
from thruflo.webapp.settings import override, override_setting

require_setting('test_module')

@require('test_function')
def foo(): # pragma: no cover
    pass


@require('test_class')
class Foo(object):
    pass
    


require_setting('test_override_function', default='something')

class TestIntegration(unittest.TestCase):
    """ Test requiring and overriding settings.
    """
    
    def setUp(self):
        """ Scan the module to actually execute the decorator.
        """
        
        from thruflo.webapp.tests import test_settings
        
        self.required_items = {
            'test_module': 'some value',
            'test_function': 'some value',
            'test_class': 'some value'
        }
        self.settings = RequirableSettings()
        self.scanner = venusian.Scanner(settings=self.settings)
        self.scanner.scan(test_settings, categories=('thruflo',))
        
    
    def test_required_items(self):
        """ This is our control: calling `self.settings` with 
          `self.required_items` should be fine.
        """
        
        self.settings(self.required_items)
        self.assertTrue(self.settings['test_module'] == 'some value')
        self.assertTrue(self.settings['test_function'] == 'some value')
        self.assertTrue(self.settings['test_class'] == 'some value')
        
    
    def test_module(self):
        """ `test_module` should be required.
        """
        
        items = self.required_items.copy()
        del items['test_module']
        self.assertRaises(
            KeyError,
            self.settings,
            items
        )
        
    
    def test_function(self):
        """ `test_function` should be required.
        """
        
        items = self.required_items.copy()
        del items['test_function']
        self.assertRaises(
            KeyError,
            self.settings,
            items
        )
        
    
    def test_class(self):
        """ `test_class` should be required.
        """
        
        items = self.required_items.copy()
        del items['test_class']
        self.assertRaises(
            KeyError,
            self.settings,
            items
        )
        
    
    def test_override(self):
        """ Test the overrides.
        """
        
        from thruflo.webapp.tests.fixtures import settings
        
        self.scanner.scan(settings, categories=('thruflo',))
        
        self.settings(self.required_items)
        self.assertTrue(self.settings['test_override_function'] == 'something else')
        
    
    

class TestVenusian(unittest.TestCase):
    """ See http://bit.ly/dIKcX9, specifically the bit that says
      
      > This has the effect that double-registrations will never 
      be performed.
      
      `thruflo.webapp.settings` is our equivalent of that article's 
      `config.py`, this module is `app.py` and `.fixtures.double_import` 
      is like `app2.py`.
    """
    
    def test_double_import(self):
        """ `app2` imports `app`, which means the `require_setting`
          above would be run twice if we executed them on import.
          
          That would throw a KeyError (as we see in the next test).
        """
        
        from thruflo.webapp.tests import test_settings
        from thruflo.webapp.tests import test_settings
        from thruflo.webapp.tests.fixtures import double_import
        
        settings = RequirableSettings()
        scanner = venusian.Scanner(settings=settings)
        
        scanner.scan(test_settings, categories=('thruflo',))
        scanner.scan(double_import, categories=('thruflo',))
        
        settings({
            'test_module': 'some value',
            'test_function': 'some value',
            'test_class': 'some value'
        })
        self.assertTrue(settings['test_module'] == 'some value')
        
    
    


