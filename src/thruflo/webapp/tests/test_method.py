#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit and integration tests for `thruflo.webapp.method`.
"""

import venusian
import unittest
from mock import Mock

from zope.interface import implements
from thruflo.webapp.interfaces import IRequestHandler

from thruflo.webapp.method import expose
from thruflo.webapp.method import ExposedMethodSelector

class MockHandler(object):
    """ Mock that the venusian scanner should pick up.
    """
    
    implements(IRequestHandler)
    
    @expose
    def yes(self):
        """ This method should be exposed.
        """
        
    
    def no(self):
        """ This method should not be exposed.
        """
        
    
    


class TestIntegration(unittest.TestCase):
    """ Test the @expose decorator.
    """
    
    def setUp(self):
        """ Scan the module to actually execute the decorator.
        """
        
        from thruflo.webapp.tests import test_method
        scanner = venusian.Scanner()
        scanner.scan(test_method, categories=('thruflo',))
        self.handler = MockHandler()
        
    
    
    def test_scanned_yes(self):
        """ `MockHandler.yes` should be exposed.
        """
        
        s = ExposedMethodSelector(self.handler)
        self.assertTrue(s.select_method('YES') == self.handler.yes)
        
    
    
    def test_scanned_no(self):
        """ `MockHandler.no` should not be exposed.
        """
        
        s = ExposedMethodSelector(self.handler)
        self.assertTrue(s.select_method('NO') is None)
        
    
    

class TestExposedMethodSelector(unittest.TestCase):
    """ Test the logic of the ExposedMethodSelector.
    """
    
    def setUp(self):
        class MockContext(object):
            __exposed_methods__ = ['a', 'b', 'C']
            a = 'method_a'
            c = 'method_c'
            
        
        self.context = MockContext()
        self.method_selector = ExposedMethodSelector(self.context)
        
    
    
    def test_init(self):
        """ `self.context` is available as `self.context` within
          the `ExposedMethodSelector` instance.
        """
        
        self.assertTrue(self.method_selector.context == self.context)
        
    
    
    def test_method_name_must_be_basestring(self):
        """ Method name must be a `basestring`.
        """
        
        self.assertRaises(
            ValueError, 
            self.method_selector.select_method,
            42
        )
        
    
    
    def test_exposed_methods_exists(self):
        """ Context must have `__exposed_methods__`.
        """
        
        class MockContext(object):
            a = 'method_a'
            c = 'method_c'
            
        
        self.method_selector = ExposedMethodSelector(MockContext())
        self.assertTrue(self.method_selector.select_method('a') == None)
        
    
    
    def test_method_exists(self):
        """ Context must have the method.
        """
        
        self.assertTrue(self.method_selector.select_method('b') == None)
        
    
    
    def test_method_exposed(self):
        """ Method must be exposed.
        """
        
        self.assertTrue(self.method_selector.select_method('c') == None)
        
    
    
    def test_select_method(self):
        """ Select method returns the method.
        """
        
        self.assertTrue(self.method_selector.select_method('a') == 'method_a')
        
    
    
    def test_force_to_lowercase(self):
        """ Method name is forced to lower case.
        """
        
        self.assertTrue(self.method_selector.select_method('A') == 'method_a')
        self.assertTrue(self.method_selector.select_method('C') == None)
        
    
    

