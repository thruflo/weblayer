#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Require specific settings to be provided to the application
  by declaring the dependency at a module, class or function level.
  
  For example, say your application code needs to know the value
  of a particular webservice api key.  You can require it by 
  calling the `require_setting` method at module level::
  
      >>> require_setting('api_key')
  
  Or by decorating a class or function (*not* a method)::
  
      >>> @require('api_key')
      ... class Foo(object): pass
      ... 
      >>> @require('api_key')
      ... def foo(self): pass
      ... 
  
  Then, once we've executed a `venusian` scan (which we fake here
  see `./tests/test_settings.py` for real integration tests)::
  
      >>> settings = RequirableSettings()
      >>> settings._require('api_key') # never call this directly!
  
  You can call the `RequirableSettings` instance with the settings
  provided.  If you pass in a value for `api_key`, great, otherwise, 
  you'll get a `KeyError`::
  
      >>> settings({})
      Traceback (most recent call last):
      ...
      KeyError: u'Required setting `api_key` () is missing'
      >>> settings({'api_key': '123'})
      >>> settings['api_key']
      '123'
  
  You can specify default values and help strings ala:
  
      require_setting('baz', default='blah', help=u'what is this?')
      settings({'api_key': '123'})
      # settings['baz'] would be 'blah'
  
  You can't require the same setting twice with different values:
  
      require_setting('baz', default='something else')
      # would raise a KeyError
  
  Unless you explicitly use `override_setting`:
  
      override_setting('baz', default='something else')
      settings({'api_key': '123'})
      # settings['baz'] would be 'something else'
  
  Which is also available as the `@override` decorator:
  
      @override('api_key', default="...")
      class Foo(object): pass
  
"""

__all__ = [
    'require',
    'override',
    'require_setting',
    'override_setting',
    'RequirableSettings'
]

import inspect
import venusian

from zope.interface import implements

from interfaces import IRequirableSettings

_HANGER_NAME = '__thruflo_require_settings_venusian_hanger__'

def require_setting(name, default=None, help=u'', category='thruflo.webapp'):
    """ Call this at module level to require a setting.
      
      Works just like a decorator, defering the real work
      until the callback is called by a `venusian` scan.
      
      However, because it's *not* a decorator, we need to
      do a little dance...
      
    """
    
    # the first step is to get the module we're being called in
    calling_mod = inspect.getmodule(inspect.stack()[1][0])
    
    # ignore when `None` (e.g.: if called from a doctest)
    if calling_mod is not None:
        # make sure it has a harmless function at
        # `calling_mod.__thruflo_require_settings_venusian_hanger__`
        def _hanger(): pass
        
        if not hasattr(calling_mod, _HANGER_NAME):
            setattr(calling_mod, _HANGER_NAME, _hanger)
        
        # defer the real business
        def callback(scanner, *args):
            return scanner.settings._require(
                name, 
                default=default, 
                help=help
            )
        
        
        # and, crucially, hang the callback off the *calling module*
        venusian.attach(
            getattr(calling_mod, _HANGER_NAME),
            callback,
            category=category
        )
    

def override_setting(name, default=None, help=u'', category='thruflo.webapp'):
    """ Call this at module level to override a setting.
    """
    
    # the first step is to get the module we're being called in
    calling_mod = inspect.getmodule(inspect.stack()[1][0])
    
    # ignore when `None` (e.g.: if called from a doctest)
    if calling_mod is not None:
        # make sure it has a harmless function at
        # `calling_mod.__thruflo_require_settings_venusian_hanger__`
        def _hanger(): pass
        
        if not hasattr(calling_mod, _HANGER_NAME):
            setattr(calling_mod, _HANGER_NAME, _hanger)
        
        # defer the real business
        def callback(scanner, *args):
            return scanner.settings._override(
                name, 
                default=default, 
                help=help
            )
        
        
        # and, crucially, hang the callback off the *calling module*
        venusian.attach(
            getattr(calling_mod, _HANGER_NAME),
            callback,
            category=category
        )
    
    


class require(object):
    """ Decorator to require a setting.
    """
    
    def __init__(self, name, default=None, help=u'', category='thruflo.webapp'):
        self._name = name
        self._default = default
        self._help = help
        self._category = category
        
    
    def __call__(self, wrapped):
        """
        """
        
        def callback(scanner, *args):
            return scanner.settings._require(
                self._name, 
                default=self._default, 
                help=self._help
            )
            
        
        venusian.attach(wrapped, callback, category=self._category)
        return wrapped
        
    
    

class override(object):
    """ Decorator to override a setting.
    """
    
    def __init__(self, name, default=None, help=u'', category='thruflo.webapp'):
        self._name = name
        self._default = default
        self._help = help
        self._category = category
        
    
    
    def __call__(self, wrapped):
        """
        """
        
        def callback(scanner, *args):
            return scanner.settings._override(
                self._name, 
                default=self._default, 
                help=self._help
            )
            
        
        venusian.attach(wrapped, callback, category=self._category)
        return wrapped
        
    
    


class RequirableSettings(object):
    """ Utility that provides dictionary-like access to 
      global application settings.
      
      Do not use the `_require` and `_override` methods directly.  
      Instead, use the `require_setting` and `override_setting`
      functions below, in tandem with a `venusian` scan.
    """
    
    implements(IRequirableSettings)
    
    def __init__(self):
        self.__required_settings__ = {}
        self._items = {}
        
    
    
    def __getitem__(self, name):
        """ Get item::
          
              >>> settings = RequirableSettings()
              >>> settings({'a': 'foobar'})
              >>> settings['a']
              'foobar'
          
        """
        
        return self._items.__getitem__(name)
        
    
    def __setitem__(self, name, value):
        """ Set item::
          
              >>> settings = RequirableSettings()
              >>> settings['a'] = 'baz'
              >>> settings['a']
              'baz'
          
        """
        
        return self._items.__setitem__(name, value)
        
    
    def __delitem__(self, name):
        """ Delete item::
          
              >>> settings = RequirableSettings()
              >>> settings({'a': 'foobar'})
              >>> settings['a']
              'foobar'
              >>> del settings['a']
              >>> settings['a']
              Traceback (most recent call last):
              ...
              KeyError: 'a'
          
        """
        
        return self._items.__delitem__(name)
        
    
    def __contains__(self, name):
        """ Contains item::
          
              >>> settings = RequirableSettings()
              >>> settings({'a': 'foobar'})
              >>> 'a' in settings
              True
              >>> 'b' in settings
              False
          
        """
        
        return self._items.__contains__(name)
        
    
    def __iter__(self):
        """ Iterate through items::
          
              >>> settings = RequirableSettings()
              >>> settings({'a': 'foobar', 'b': ''})
              >>> for k in settings:
              ...     k
              'a'
              'b'
          
        """
        
        return self._items.__iter__()
        
    
    
    def _require(self, name, default=None, help=u''):
        """ Require an application setting.
          
          Defaults to None::
          
              >>> settings = RequirableSettings()
              >>> settings._require('a')
              >>> settings.__required_settings__['a']
              (None, u'')
          
          Unless passed in::
          
              >>> settings._require('b', default='b', help=u'help msg')
              >>> settings.__required_settings__['b']
              ('b', u'help msg')
          
          You can call `require` as many times as you like::
          
              >>> settings = RequirableSettings()
              >>> settings._require('a')
              >>> settings._require('a')
              >>> settings._require('a')
              >>> settings.__required_settings__
              {'a': (None, u'')}
          
          But you can't require the same setting *with different values*::
          
              >>> settings._require('a', default='a')
              Traceback (most recent call last):
              ...
              KeyError: u'a is already defined'
          
          Whether that means the default value (above) or the help message::
          
              >>> settings._require('a', help=u'elephants')
              Traceback (most recent call last):
              ...
              KeyError: u'a is already defined'
          
        """
        
        if name in self.__required_settings__:
            if self.__required_settings__[name] != (default, help):
                raise KeyError(u'{} is already defined'.format(name))
        
        self.__required_settings__[name] = (default, help)
        
    
    def _override(self, name, default=None, help=u''):
        """ Require a setting regardless of whether it has already
          been required or not.
          
          Defaults to None::
          
              >>> settings = RequirableSettings()
              >>> settings._override('a')
              >>> settings.__required_settings__['a']
              (None, u'')
          
          Unless passed in::
          
              >>> settings._override('b', default='b', help=u'help msg')
              >>> settings.__required_settings__['b']
              ('b', u'help msg')
          
          With `override`, you can require the same settings twice with 
          different values::
          
              >>> settings._override('a', default='a')
              >>> settings.__required_settings__['a']
              ('a', u'')
              >>> settings._override('a', help=u'elephants')
              >>> settings.__required_settings__['a']
              (None, u'elephants')
          
        """
        
        self.__required_settings__[name] = (default, help)
        
    
    
    def __call__(self, items):
        """ `items` are checked against `self.__required_settings__`.
          If any required settings are missing, if they were declared
          with a default value, the setting is set up with the
          default value::
          
              >>> settings = RequirableSettings()
              >>> reqs = {'a': ('a', u'help msg a'), 'b': ('b', u'help msg b')}
              >>> settings.__required_settings__ = reqs
              >>> settings()
              Traceback (most recent call last):
              ...
              TypeError: __call__() takes exactly 2 arguments (1 given)
              >>> settings({'a': 'foobar'})
              >>> settings['a']
              'foobar'
              >>> settings['b']
              'b'
          
          Otherwise we throw a KeyError.
          
              >>> reqs = {'a': (None, u'help msg a'), 'b': ('b', u'help msg b')}
              >>> settings.__required_settings__ = reqs
              >>> settings({})
              Traceback (most recent call last):
              ...
              KeyError: u'Required setting `a` (help msg a) is missing'
          
        """
        
        missing = []
        for k, v in self.__required_settings__.iteritems():
            if not k in items:
                default = v[0]
                if default is not None:
                    self[k] = default
                else:
                    msg = u'Required setting `{}` ({}) is missing'.format(k, v[1])
                    missing.append(msg)
        if missing:
            raise KeyError(u', '.join(missing))
        
        for k, v in items.iteritems():
            self[k] = v
            
        
    
    

