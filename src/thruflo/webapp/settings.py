#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Notes:
  
  - we want to use paste's parsing, so settings need to get
    setup in, e.g.: `Bootstrapper().set_settings(settings)`
  - settings could then be available via a simple 
    `getUtility(ISettings)`
  
  - however, `define()` is also a nice pattern to declare 
    required settings -- or is it?  do we just simple use
    an interface?  or do we make it a decorator?
  - perhaps if we do `define` we could then add the module
    name as a path, e.g.: `settings.template.directories`
  
"""

from zope.interface import implements

from interfaces import IApplicationSettings

class ApplicationSettings(object):
    """ Utility that provides dictionary-like access to 
      global application settings.
      
      Provides `require` and `override` classmethods that
      can be used to declare required settings and their
      potential default values.
      
    """
    
    implements(IApplicationSettings)
    
    __required_settings__ = {}
    
    _items = {}
    
    def __init__(self, items):
        """ When `ApplicationSettings` is initiated, the `items`
          are checked against the required settings.  If any
          required settings are missing, if they were declared
          with a default value, the setting is set up with the
          default value, otherwise we throw a KeyError.
        """
        
        missing = []
        for k, v in self.__required_settings__:
            if not k in items:
                default = v[0]
                if default is not None:
                    self[k] = default
                else:
                    msg = u'Required setting `{}` ({}) is missing'.format(k, v[1])
                    missing.append(msg)
        if missing:
            raise KeyError(u', '.join(missing))
            
        for k, v in items:
            self[k] = v
            
        
    
    
    def __getitem__(self, name):
        return self._items.__getitem__(name)
        
    
    def __setitem__(self, name, value):
        return self._items.__setitem__(name, value)
        
    
    def __delitem__(self, name):
        """ Delete item.
        """
        
        return self._items.__delitem__(name)
        
    
    def __contains__(self, name):
        """ Contains item.
        """
        
        return self._items.__contains__(name)
        
    
    def __iter__(self):
        """ Iterate.
        """
        
        return self._items.__iter__()
        
    
    
    @classmethod
    def require(cls, name, default=None, help=u''):
        """ Require an application setting.
        """
        
        if name in cls.__required_settings__:
            raise KeyError(u'{} is already defined')
        
        cls.__required_settings__[name] = (default, help)
        
    
    @classmethod
    def override(cls, name, default=None, help=u''):
        """ Require a setting regardless of whether it has already
          been required or not.
        """
        
        cls.__required_settings__[name] = (default, help)
        
    
    


require_setting = ApplicationSettings.require
override_setting = ApplicationSettings.override
