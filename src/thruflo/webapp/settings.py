#!/usr/bin/env python
# -*- coding: utf-8 -*-

raise NotImplementedError(
    """ settings.py is currently in a bit of a mess.
      
      The previous impl had classmethods, a global __required_settings__
      and the items going in to the __init__
      
      It seems that perhaps we should instantiate an empty settings
      object, pass it to the venusian scanner, add the required
      settings to a single instance and then pass in the parsed
      items.
      
      The second question is whether then to use functions, decorators
      or both to populate the required settings.  Perhaps it makes
      sense to provide both?
      
      The current doctests and test_settings are mid work...
    """
)

""" Settings that can be required on a module by module basis.
  
  For example, say your application code needs to know the value
  of a particular webservice api key.  You can require it by
  writing `require_setting('foobar_api_key')` at module level.
  
  Then, when you initiate `RequirableSettings`, if you pass in
  a value for `foobar_api_key`, great::
  
      >>> s = RequirableSettings({'foobar_api_key': '123'})
      >>> s['foobar_api_key']
      '123'
  
  Otherwise, you'll get a `KeyError`::
  
      >>> s = RequirableSettings({})
      Traceback (most recent call last):
      ...
      KeyError: u'Required setting `foobar_api_key` () is missing'
      
  You can specify default values and help strings::
  
      >>> require_setting('baz', default='blah', help=u'what is this?')
      >>> s = RequirableSettings({'foobar_api_key': '123'})
      >>> s['baz']
      'blah'
  
  You can't require the same setting twice with different values::
  
      >>> require_setting('baz', default='something else')
      Traceback (most recent call last):
      ...
      KeyError: u'baz is already defined'
  
  Unless you explicitly use `override_setting`::
  
      >>> override_setting('baz', default='something else')
      >>> s = RequirableSettings({'foobar_api_key': '123'})
      >>> s['baz']
      'something else'
  
"""

__all__ = [
    'RequirableSettings'
]

import venusian

from zope.interface import implements

from interfaces import ISettings

class RequirableSettings(object):
    """ Utility that provides dictionary-like access to 
      global application settings.
      
      Do not use the `_require` and `_override` classmethods directly.  
      Instead, use the `require_setting` and `override_setting`
      functions below, in tandem with a `venusian` scan.
    """
    
    implements(ISettings)
    
    __required_settings__ = {}
    
    def __init__(self, items):
        """ `items` are checked against `__required_settings__`.
          If any required settings are missing, if they were declared
          with a default value, the setting is set up with the
          default value::
          
              >>> s = {'a': ('a', u'help msg a'), 'b': ('b', u'help msg b')}
              >>> RequirableSettings.__required_settings__ = s
              >>> settings = RequirableSettings()
              Traceback (most recent call last):
              ...
              TypeError: __init__() takes exactly 2 arguments (1 given)
              >>> settings = RequirableSettings({'a': 'foobar'})
              >>> settings['a']
              'foobar'
              >>> settings['b']
              'b'
          
          Otherwise we throw a KeyError.
              
              >>> s = {'a': (None, u'help msg a'), 'b': ('b', u'help msg b')}
              >>> RequirableSettings.__required_settings__ = s
              >>> RequirableSettings({})
              Traceback (most recent call last):
              ...
              KeyError: u'Required setting `a` (help msg a) is missing'
          
        """
        
        self._items = {}
        
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
            
        
    
    def __getitem__(self, name):
        """ Get item::
          
              >>> RequirableSettings.__required_settings__ = {}
              >>> settings = RequirableSettings({'a': 'foobar'})
              >>> settings['a']
              'foobar'
          
        """
        
        return self._items.__getitem__(name)
        
    
    def __setitem__(self, name, value):
        """ Set item::
          
              >>> RequirableSettings.__required_settings__ = {}
              >>> settings = RequirableSettings({'a': 'foobar'})
              >>> settings['a'] = 'baz'
              >>> settings['a']
              'baz'
          
        """
        
        return self._items.__setitem__(name, value)
        
    
    def __delitem__(self, name):
        """ Delete item::
          
              >>> RequirableSettings.__required_settings__ = {}
              >>> settings = RequirableSettings({'a': 'foobar'})
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
          
              >>> RequirableSettings.__required_settings__ = {}
              >>> settings = RequirableSettings({'a': 'foobar'})
              >>> 'a' in settings
              True
              >>> 'b' in settings
              False
          
        """
        
        return self._items.__contains__(name)
        
    
    def __iter__(self):
        """ Iterate through items::
          
              >>> RequirableSettings.__required_settings__ = {}
              >>> settings = RequirableSettings({'a': 'foobar', 'b': ''})
              >>> for k in settings:
              ...     k
              'a'
              'b'
          
        """
        
        return self._items.__iter__()
        
    
    
    @classmethod
    def _require(cls, name, default=None, help=u''):
        """ Require an application setting.
          
          Defaults to None::
          
              >>> RequirableSettings.__required_settings__ = {}
              >>> RequirableSettings._require('a')
              >>> RequirableSettings.__required_settings__['a']
              (None, u'')
          
          Unless passed in::
          
              >>> RequirableSettings.require('b', default='b', help=u'help msg')
              >>> RequirableSettings.__required_settings__['b']
              ('b', u'help msg')
          
          You can call `require` as many times as you like::
          
              >>> RequirableSettings._require('a')
              >>> RequirableSettings._require('a')
              >>> RequirableSettings._require('a')
              >>> RequirableSettings._require('a')
              >>> RequirableSettings.__required_settings__['a']
              (None, u'')
          
          But you can't require the same setting *with different values*::
          
              >>> RequirableSettings._require('a')
              >>> RequirableSettings._require('a', default='a')
              Traceback (most recent call last):
              ...
              KeyError: u'a is already defined'
              >>> RequirableSettings._require('a', help=u'elephants')
              Traceback (most recent call last):
              ...
              KeyError: u'a is already defined'
          
          This allows for multiple module level imports to sail through
          but hopefully helps catch user error where the same setting
          is defined twice (@@ this could be enforced rather more
          stringently...).
        """
        
        if name in cls.__required_settings__:
            if cls.__required_settings__[name] != (default, help):
                raise KeyError(u'{} is already defined'.format(name))
        
        cls.__required_settings__[name] = (default, help)
        
    
    @classmethod
    def _override(cls, name, default=None, help=u''):
        """ Require a setting regardless of whether it has already
          been required or not.
          
          Defaults to None::
          
              >>> RequirableSettings.__required_settings__ = {}
              >>> RequirableSettings._override('a')
              >>> RequirableSettings.__required_settings__['a']
              (None, u'')
          
          Unless passed in::
          
              >>> RequirableSettings._override('b', default='b', help=u'help msg')
              >>> RequirableSettings.__required_settings__['b']
              ('b', u'help msg')
          
          With `override`, you can require the same settings twice with 
          different values::
          
              >>> RequirableSettings._override('a', default='a')
              >>> RequirableSettings.__required_settings__['a']
              ('a', u'')
              >>> RequirableSettings._override('a', help=u'elephants')
              >>> RequirableSettings.__required_settings__['a']
              (None, u'elephants')
              
          
        """
        
        cls.__required_settings__[name] = (default, help)
        
    
    


def _a_harmless_function():
    pass
    

def require_setting(name, default=None, help=u'', venusian=venusian):
    """
    """
    
    def callback(*args):
        return RequirableSettings._require(name, default=None, help=u'')
        
    
    venusian.attach(_a_harmless_function, callback, category='thruflo')
    

def override_setting(name, default=None, help=u'', venusian=venusian):
    """
    """
    
    def callback(*args):
        return RequirableSettings._override(name, default=None, help=u'')
        
    
    
    venusian.attach(_a_harmless_function, callback, category='thruflo')
    


