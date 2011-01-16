#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" :py:mod:`weblayer.settings` provides :py:class:`RequirableSettings`, an 
  implementation of :py:class:`~weblayer.interfaces.ISettings` that allows you
  to (optionally) declare the settings that your application requires.
  
  For example, say your application code needs to know the value of a
  particular webservice api key.  You can require it by calling the 
  :py:func:`require_setting` method (by convention at the top of a module, so
  the requirement is clear)::
  
      >>> require_setting('api_key')
  
  Or by decorating a function or method with :py:func:`require`::
  
      >>> class Foo(object):
      ...     @require('api_key')
      ...     def foo(self):
      ...         pass
      ...     
      ... 
      >>> @require('api_key')
      ... def foo(self): pass
      ... 
  
  Then, once we've executed a `venusian scan`_ (which we fake here: see 
  `./tests/test_settings.py`_ for real integration tests)::
  
      >>> settings = RequirableSettings()
      >>> def mock_require_setting(*args, **kwargs):
      ...     settings._require(*args, **kwargs) # never call this directly!
      ... 
      >>> def mock_override_setting(*args, **kwargs):
      ...     settings._override(*args, **kwargs) # never call this directly!
      ... 
      >>> mock_require_setting('api_key')
  
  You can call the :py:class:`RequirableSettings` instance with a dictionary
  of settings provided by the user / your application.  If you pass in a value
  for ``api_key``, great, otherwise, you'll get a ``KeyError``::
  
      >>> settings({'api_key': '123'})
      >>> settings['api_key']
      '123'
      >>> settings({})
      Traceback (most recent call last):
      ...
      KeyError: u'Required setting `api_key` () is missing'
  
  You can specify default values and help strings ala::
  
      >>> mock_require_setting('baz', default='blah', help=u'what is this?')
      >>> settings({'api_key': '123'})
      >>> settings['baz']
      'blah'
  
  You can't require the same setting twice with different values::
  
      >>> mock_require_setting('baz', default='something else')
      Traceback (most recent call last):
      ...
      KeyError: u'baz is already defined'
  
  Unless you explicitly use :py:func:`override_setting` (also available as the
  :py:func:`override` decorator):
  
      >>> mock_override_setting('baz', default='something else')
      >>> settings({'api_key': '123'})
      >>> settings['baz']
      'something else'
  
  .. _`venusian scan`: http://docs.repoze.org/venusian/
  .. _`./tests/test_settings.py`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/tests/test_settings.py
"""

__all__ = [
    'RequirableSettings',
    'require_setting',
    'require',
    'override_setting',
    'override'
]

import inspect
import venusian

from UserDict import DictMixin

from zope.interface import implements

from interfaces import ISettings

_CATEGORY = 'weblayer'
_HANGER_NAME = '__weblayer_require_settings_venusian_hanger__'

class RequirableSettings(object, DictMixin):
    """ Utility that provides dictionary-like access to application settings.
      
      Do not use the ``_require`` and ``_override`` methods directly.  Instead,
      use the :py:func:`require_setting` and :py:func:`override_setting`
      functions or the :py:func:`require` and :py:func:`override` decorators.
      
      Note that the 
    """
    
    implements(ISettings)
    
    def __init__(self, packages=None, extra_categories=None):
        """ If ``packages``, run a `venusian scan`_.
          
          .. _`venusian scan`: http://docs.repoze.org/venusian/
        """
        
        self.__required_settings__ = {}
        self._items = {}
        
        if packages:
            categories = [_CATEGORY]
            if extra_categories is not None:
                categories.extend(extra_categories)
            scanner = venusian.Scanner(settings=self)
            for item in packages:
                scanner.scan(item, categories=categories)
                
            
        
        
    
    
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
        
    
    def keys(self):
        """ Return keys::
          
              >>> settings = RequirableSettings()
              >>> settings({'a': None, 'b': None})
              >>> settings.keys()
              ['a', 'b']
          
        """
        
        return self._items.keys()
        
    
    def __repr__(self):
        """ Represent class and items::
          
              >>> settings = RequirableSettings()
              >>> settings
              <weblayer.settings.RequirableSettings {}>
              >>> settings({'a': 'foobar', 'b': ''})
              >>> settings
              <weblayer.settings.RequirableSettings {'a': 'foobar', 'b': ''}>
          
        """
        
        return u'<weblayer.settings.RequirableSettings %s>' % (self._items)
        
    
    
    def _require(self, name, default=None, help=u''):
        """ Require an application setting.
          
          Defaults to ``None``::
          
              >>> settings = RequirableSettings()
              >>> settings._require('a')
              >>> settings.__required_settings__['a']
              (None, u'')
          
          Unless passed in::
          
              >>> settings._require('b', default='b', help=u'help msg')
              >>> settings.__required_settings__['b']
              ('b', u'help msg')
          
          You can call ``require`` as many times as you like::
          
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
                raise KeyError(u'%s is already defined' % name)
        
        self.__required_settings__[name] = (default, help)
        
    
    def _override(self, name, default=None, help=u''):
        """ Require a setting regardless of whether it has already been
          required or not.
          
          Defaults to ``None``::
          
              >>> settings = RequirableSettings()
              >>> settings._override('a')
              >>> settings.__required_settings__['a']
              (None, u'')
          
          Unless passed in::
          
              >>> settings._override('b', default='b', help=u'help msg')
              >>> settings.__required_settings__['b']
              ('b', u'help msg')
          
          With ``override``, you can require the same settings twice with 
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
        """ ``items`` are checked against ``self.__required_settings__``.
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
          
          Otherwise we throw a ``KeyError``.
          
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
                    msg = u'Required setting `%s` (%s) is missing' % (k, v[1])
                    missing.append(msg)
        if missing:
            raise KeyError(u', '.join(missing))
        
        for k, v in items.iteritems():
            self[k] = v
            
        
    
    


def _attach_callback(
        name, 
        default=None, 
        help=u'', 
        category=_CATEGORY,
        override=False
    ):
    """ Hangs a callback to ``_require`` or ``_override`` off the module that
      this method is called from.
      
      Attaches the callback manually, rather than using `venusian.attach`_ so
      that :ref:`weblayer` doesn't depend on a 
      `CPython implementation detail`_.
          
      .. `venusian.attach`_: http://svn.repoze.org/venusian/trunk/venusian/__init__.py
      .. _`CPython implementation detail`: http://docs.python.org/library/sys.html#sys._getframe
    """
    
    # get the module we're being called in
    calling_mod = None
    for item in inspect.stack():
        if item[3] == '<module>':
            calling_mod = inspect.getmodule(item[0])
            break
        
    # ignore when `None` (e.g.: if called from a doctest)
    if calling_mod is None:
        return
    
    # make sure it has a harmless function at
    # `calling_mod.__weblayer_require_settings_venusian_hanger__`
    def _required_settings_hanger(): pass
    
    if not hasattr(calling_mod, _HANGER_NAME):
        setattr(calling_mod, _HANGER_NAME, _required_settings_hanger)
    
    # defer the real business
    def callback(scanner, *args):
        settings = scanner.settings
        method = override and settings._override or settings._require
        return method(name, default=default, help=help)
        
    
    hanger = getattr(calling_mod, _HANGER_NAME)
    categories = getattr(hanger, venusian.ATTACH_ATTR, {})
    callbacks = categories.setdefault(category, [])
    callbacks.append(callback)
    setattr(hanger, venusian.ATTACH_ATTR, categories)
    

def require_setting(name, default=None, help=u'', category=_CATEGORY):
    """ Require a setting.
    """
    
    _attach_callback(
        name, 
        default=default, 
        help=help, 
        category=category, 
        override=False
    )
    

def override_setting(name, default=None, help=u'', category=_CATEGORY):
    """ Override a setting.
    """
    
    _attach_callback(
        name, 
        default=default, 
        help=help, 
        category=category, 
        override=True
    )
    

def require(name, default=None, help=u'', category=_CATEGORY):
    """ Decorator to require a setting.
    """
    
    def wrap(wrapped):
        """ Called at decoration time.  Requires the setting and returns the
          unchanged wrapped function / method or class.
        """
        
        require_setting(name, default=default, help=help, category=category)
        return wrapped
        
    
    return wrap
    

def override(name, default=None, help=u'', category=_CATEGORY):
    """ Decorator to override a setting.
    """
    
    def wrap(wrapped):
        """ Called at decoration time.  Overrides the setting and returns the
          unchanged wrapped function / method or class.
        """
        
        override_setting(name, default=default, help=help, category=category)
        return wrapped
        
    
    return wrap
    

