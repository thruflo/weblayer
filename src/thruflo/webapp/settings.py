#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Settings that can be required on a module by module basis.
  
      >>> # doctest setup
      >>> RequirableSettings.__required_settings__ = {} 
  
  For example, say your application code needs to know the value
  of a particular webservice api key.  You can require it by
  writing this as module level (e.g.: call the function just below
  your module level imports)::
  
      >>> # import blah, baz ...
      >>> 
      >>> require_setting('foobar_api_key')
      >>>
      >>> # ... carry on with your module
  
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

from zope.interface import implements

from interfaces import ISettings

class RequirableSettings(object):
    """ Utility that provides dictionary-like access to 
      global application settings.
      
      Provides `require` and `override` classmethods that
      can be used to declare required settings and their
      potential default values.
      
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
        """ Contains item::
          
              >>> RequirableSettings.__required_settings__ = {}
              >>> settings = RequirableSettings({'a': 'foobar', 'b': ''})
              >>> for k in settings:
              ...     k
              'a'
              'b'
          
        """
        
        return self._items.__iter__()
        
    
    
    @classmethod
    def require(cls, name, default=None, help=u''):
        """ Require an application setting.
          
          Defaults to None::
          
              >>> RequirableSettings.__required_settings__ = {}
              >>> RequirableSettings.require('a')
              >>> RequirableSettings.__required_settings__['a']
              (None, u'')
          
          Unless passed in::
          
              >>> RequirableSettings.require('b', default='b', help=u'help msg')
              >>> RequirableSettings.__required_settings__['b']
              ('b', u'help msg')
          
          You can call `require` as many times as you like::
          
              >>> RequirableSettings.require('a')
              >>> RequirableSettings.require('a')
              >>> RequirableSettings.require('a')
              >>> RequirableSettings.require('a')
              >>> RequirableSettings.__required_settings__['a']
              (None, u'')
          
          But you can't require the same setting *with different values*::
          
              >>> RequirableSettings.require('a')
              >>> RequirableSettings.require('a', default='a')
              Traceback (most recent call last):
              ...
              KeyError: u'a is already defined'
              >>> RequirableSettings.require('a', help=u'elephants')
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
    def override(cls, name, default=None, help=u''):
        """ Require a setting regardless of whether it has already
          been required or not.
          
          Defaults to None::
          
              >>> RequirableSettings.__required_settings__ = {}
              >>> RequirableSettings.override('a')
              >>> RequirableSettings.__required_settings__['a']
              (None, u'')
          
          Unless passed in::
          
              >>> RequirableSettings.override('b', default='b', help=u'help msg')
              >>> RequirableSettings.__required_settings__['b']
              ('b', u'help msg')
          
          With `override`, you can require the same settings twice with 
          different values::
          
              >>> RequirableSettings.override('a', default='a')
              >>> RequirableSettings.__required_settings__['a']
              ('a', u'')
              >>> RequirableSettings.override('a', help=u'elephants')
              >>> RequirableSettings.__required_settings__['a']
              (None, u'elephants')
              
          
        """
        
        cls.__required_settings__[name] = (default, help)
        
    
    


require_setting = RequirableSettings.require
override_setting = RequirableSettings.override
