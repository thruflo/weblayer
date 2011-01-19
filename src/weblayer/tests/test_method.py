#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for `weblayer.method`.
"""

import unittest

try: # pragma: no cover
    from mock import Mock
except: # pragma: no cover
    pass

class TestExposedMethodSelector(unittest.TestCase):
    """ Test the logic of the ExposedMethodSelector.
    """
    
    def setUp(self):
        """
        """
        
        from weblayer.method import ExposedMethodSelector
        
        class MockContext(object):
            __all__ = ['a', 'b', 'C']
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
        """ Context must have `__all__`.
        """
        
        from weblayer.method import ExposedMethodSelector
        
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
        
    
    

class TestHEADSpecialCase(unittest.TestCase):
    """ Test special casing HEAD requests to use ``def get()`` iff:
      
      * ``'head'`` is exposed
      * ``def get()`` exists
      * ``def head()`` doesn't
      
    """
    
    def make_one(self, context):
        from weblayer.method import ExposedMethodSelector
        return ExposedMethodSelector(context)
        
    
    def test_head_not_exposed(self):
        """ When ``'head'`` isn't exposed, selecting it will return ``None``.
        """
        
        class MockContext(object):
            __all__ = ['get']
            get = 'method_get'
            
        
        
        method_selector = self.make_one(MockContext())
        method = method_selector.select_method('head')
        self.assertTrue(method is None)
        
    
    def test_head_exposed_get_not_exposed(self):
        """ When ``'head'`` is exposed but ``'get'`` isn't, selecting 
          ``'head'`` will return ``None``.
        """
        
        class MockContext(object):
            __all__ = ['head']
            get = 'method_get'
        
        
        method_selector = self.make_one(MockContext())
        method = method_selector.select_method('head')
        self.assertTrue(method is None)
        
    
    def test_head_exposed_get_exposed_get_not_defined(self):
        """ When ``'head'`` is exposed but ``def get()`` isn't defined,
          selecting ``'head'`` will return ``None``.
        """
        
        class MockContext(object):
            __all__ = ['head', 'get']
            
        
        
        method_selector = self.make_one(MockContext())
        method = method_selector.select_method('head')
        self.assertTrue(method is None)
        
    
    def test_head_exposed_get_exposed_get_defined(self):
        """ When ``'head'`` is exposed and ``def get()`` is defined,
          selecting ``'head'`` will return it.
        """
        
        class MockContext(object):
            __all__ = ['head', 'get']
            get = 'method_get'
        
        
        method_selector = self.make_one(MockContext())
        method = method_selector.select_method('head')
        self.assertTrue(method is 'method_get')
        
    
    def test_head_exposed_head_defined(self):
        """ Unless, of course, ``def head()`` is defined.
        """
        
        class MockContext(object):
            __all__ = ['head', 'get']
            get = 'method_get'
            head = 'method_head'
        
        
        method_selector = self.make_one(MockContext())
        method = method_selector.select_method('head')
        self.assertTrue(method is 'method_head')
        
    
