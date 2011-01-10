#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" :py:mod:`weblayer.static` provides 
  :py:class:`MemoryCachedStaticURLGenerator`, an implementation of
  :py:class:`~weblayer.interfaces.IStaticURLGenerator`.
  
  :py:class:`MemoryCachedStaticURLGenerator` adapts an 
  :py:class:`~weblayer.interfaces.IRequest` and requires two 
  :py:mod:`~weblayer.settings`, :py:obj:`settings['static_files_path']` and 
  :py:obj:`settings['static_url_prefix']` (which defaults to 
  :py:obj:`u'/static/'`).  
  
      >>> from mock import Mock
      >>> request = Mock()
      >>> request.host_url = 'http://static.foo.com'
      >>> settings = {}
      >>> settings['static_files_path'] = '/var/www/static'
      >>> settings['static_url_prefix'] = u'/static/'
      >>> MemoryCachedStaticURLGenerator._cache = {}
      >>> static = MemoryCachedStaticURLGenerator(request, settings)
      >>> static._cache_path = Mock()
  
  When :py:meth:`~MemoryCachedStaticURLGenerator.get_url` is called, it looks
  for a file at the :py:obj:`path` passed in, relative to 
  :py:obj:`settings['static_files_path']`.  If the file exists, it hashes it
  and appends the first few characters of the hash digest to the returned url.
  
  For example, imagine we've hashed and cached `/var/www/static/foo.js`::
  
      >>> static._cache['/var/www/static/foo.js'] = 'abcdefghijkl'
  
  The static URL returned is::
  
      >>> static.get_url('foo.js')
      u'http://static.foo.com/static/foo.js?v=abcdefg'
  
  As the :py:class:`MemoryCachedStaticURLGenerator` name suggests, the hash
  digests are cached in memory using a static class attribute.  This means
  that:
  
  * `multiple threads`_ can all access the same cache
  * `multiple processes`_ each have to populate their own cache 
  * each time the application is restarted, the cache is cleared
  
  The last two points mean that applications serving static files may incur
  CPU and memory overhead that could be avoided using a dedicated cache (like,
  `memcached`_ or `redis`_).  Production systems thus may want to provide their
  own :py:class:`~weblayer.interfaces.IStaticURLGenerator` implementation, 
  (potentially by subclassing 
  :py:class:`~weblayer.static.MemoryCachedStaticURLGenerator` and overriding
  the :py:meth:`~MemoryCachedStaticURLGenerator._cache_path` method).
  
  .. note::
  
      Alternative implementations must consider invalidating the hash
      digests when files change.  One benefit of the default 
      :py:class:`~weblayer.static.MemoryCachedStaticURLGenerator` implementation
      is that, as hash digests are invalidated when the application restarts,
      deployment setups that watch for changes to the underlying source code and 
      restart when files change cause the cache to be invalidated.
      
      For example, one way to integrate with `paste.reloader`_ so it reloaded your
      application every time a cached file changed would be to use::
      
          paster serve --reload
      
      With::
      
          def watch_cached_static_files():
              return MemoryCachedStaticURLGenerator._cache.keys()
      
          paste.reloader.add_file_callback(watch_cached_static_files)
      
  
  .. _`multiple threads`: http://docs.python.org/library/threading.html
  .. _`multiple processes`: http://docs.python.org/library/multiprocessing.html
  .. _`memcached`: http://memcached.org/
  .. _`redis`: http://redis.io/
  .. _`paste.reloader`: http://pythonpaste.org/modules/reloader.html
"""

__all__ = [
    'MemoryCachedStaticURLGenerator'
]

import logging
from os.path import join

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequest, ISettings, IStaticURLGenerator
from settings import require_setting
from utils import generate_hash

require_setting('static_files_path')
require_setting('static_url_prefix', default=u'/static/')

class MemoryCachedStaticURLGenerator(object):
    """ Adapter to generate static URLs from a request.
    """
    
    _cache = {}
    
    adapts(IRequest, ISettings)
    implements(IStaticURLGenerator)
    
    def __init__(
            self, 
            request,
            settings,
            join_path_=None, 
            open_file_=None, 
            generate_hash_=None
        ):
        """ `request.host_url` is available as `self._host_url`::
          
              >>> from mock import Mock
              >>> req = Mock()
              >>> req.host_url = 'foo.com'
              >>> settings = {}
              >>> settings['static_files_path'] = '/var/www/static'
              >>> settings['static_url_prefix'] = u'/static/'
              >>> static = MemoryCachedStaticURLGenerator(
              ...     req, 
              ...     settings
              ... )
              >>> static._host_url
              'foo.com'
          
          `settings['static_files_path']` and `settings['static_url_prefix']` are
          available as `self._static_files_path` and `self._static_url_prefix`::
          
              >>> static = MemoryCachedStaticURLGenerator(
              ...     req, 
              ...     settings
              ... )
              >>> static._static_files_path
              '/var/www/static'
              >>> static._static_url_prefix
              u'/static/'
          
          `join_path_` defaults to `join` and is available as 
          `self._join_path`::
          
              >>> static = MemoryCachedStaticURLGenerator(req, settings)
              >>> static._join_path == join
              True
              >>> static = MemoryCachedStaticURLGenerator(
              ...     req, 
              ...     settings, 
              ...     join_path_='join'
              ... )
              >>> static._join_path
              'join'
          
          `open_file_` defaults to `open` and is available as 
          `self._open_file`::
          
              >>> static = MemoryCachedStaticURLGenerator(req, settings)
              >>> static._open_file == open
              True
              >>> static = MemoryCachedStaticURLGenerator(
              ...     req, 
              ...     settings, 
              ...     open_file_='open'
              ... )
              >>> static._open_file
              'open'
          
          `generate_hash_` defaults to `generate_hash` and is available as 
          `self._generate_hash`::
          
              >>> static = MemoryCachedStaticURLGenerator(req, settings)
              >>> static._generate_hash == generate_hash
              True
              >>> static = MemoryCachedStaticURLGenerator(
              ...     req, 
              ...     settings, 
              ...     generate_hash_='generate'
              ... )
              >>> static._generate_hash
              'generate'
          
        """
        
        self._host_url = request.host_url
        self._static_files_path = settings['static_files_path']
        self._static_url_prefix = settings['static_url_prefix']
        
        if join_path_ is None:
            self._join_path = join
        else:
            self._join_path = join_path_
        
        if open_file_ is None:
            self._open_file = open
        else:
            self._open_file = open_file_
        
        if generate_hash_ is None:
            self._generate_hash = generate_hash
        else:
            self._generate_hash = generate_hash_
        
    
    def _cache_path(self, file_path):
        """ Expand the request `path` into a `file_path`, check to see if
          it exists, if it does, hash it and store the `digest` against
          the `path` in the `_cache`.
          
              >>> from mock import Mock
              >>> from StringIO import StringIO
              >>> request = Mock()
              >>> open_file = Mock()
              >>> sock = StringIO()
              >>> open_file.return_value = sock
              >>> generate_hash = Mock()
              >>> generate_hash.return_value = 'digest'
              >>> settings = {
              ...     'static_files_path': '/var/www/static', 
              ...     'static_url_prefix': u'/static/'
              ... }
              >>> static = MemoryCachedStaticURLGenerator(
              ...     request, 
              ...     settings,
              ...     open_file_=open_file,
              ...     generate_hash_=generate_hash
              ... )
              >>> static._cache_path('/var/www/static/foo.js')
          
          If `file_path` exists::
          
              >>> open_file.assert_called_with('/var/www/static/foo.js')
          
          It's hashed::
          
              >>> generate_hash.assert_called_with(s=sock)
          
          The hash is cached::
          
              >>> static._cache['/var/www/static/foo.js']
              'digest'
          
          Unless the file_path can't be opened::
          
              >>> def open_file(file_path):
              ...     raise IOError
              ... 
              >>> static = MemoryCachedStaticURLGenerator(
              ...     request, 
              ...     settings,
              ...     open_file_=open_file,
              ...     generate_hash_=generate_hash
              ... )
              >>> static._cache_path('/var/www/static/foo.js')
              >>> static._cache['/var/www/static/foo.js'] is None
              True
          
        """
        
        try:
            sock = self._open_file(file_path)
        except IOError:
            logging.warning(u'Couldn\'t open static file %s' % file_path)
            self._cache[file_path] = None
        else:
            digest = self._generate_hash(s=sock)
            sock.close()
            self._cache[file_path] = digest
        
    
    def get_url(self, path, snip_digest_at=7):
        """ Get a fully expanded url for the given static resource :py:obj:`path`::
          
              >>> from mock import Mock
              >>> request = Mock()
              >>> request.host_url = 'http://static.foo.com'
              >>> settings = {}
              >>> settings['static_files_path'] = '/var/www/static'
              >>> settings['static_url_prefix'] = u'/static/'
              >>> join_path = Mock()
              >>> join_path.return_value = '/var/www/static/foo.js'
              >>> MemoryCachedStaticURLGenerator._cache = {}
              >>> static = MemoryCachedStaticURLGenerator(
              ...     request, 
              ...     settings,
              ...     join_path_=join_path
              ... )
              >>> static._cache_path = Mock()
          
          :py:obj:`path` is expanded into :py:obj:`file_path`::
          
              >>> url = static.get_url('foo.js')
              >>> join_path.assert_called_with('/var/www/static', 'foo.js')
          
          If :py:obj:`path` isn't in :py:attr:`self._cache`, calls 
          :py:meth:`self._cache_path`::
          
              >>> static._cache_path.assert_called_with('/var/www/static/foo.js')
          
          If the digest is :py:obj:`None`, just joins the host url, prefix and
          path::
          
              >>> static._cache['/var/www/static/foo.js'] = None
              >>> static.get_url('foo.js')
              u'http://static.foo.com/static/foo.js'
          
          Else also appends :py:obj:`'?v='` plus upto the first 
          :py:obj:`snip_digest_at` chars of the digest, which defaults to 
          :py:obj:`7`::
          
              >>> static._cache['/var/www/static/foo.js'] = 'abcdefghijkl'
              >>> static.get_url('foo.js')
              u'http://static.foo.com/static/foo.js?v=abcdefg'
              >>> static.get_url('foo.js', snip_digest_at=4)
              u'http://static.foo.com/static/foo.js?v=abcd'
          
          Cleanup::
          
              >>> MemoryCachedStaticURLGenerator._cache = {}
          
        """
        
        file_path = self._join_path(self._static_files_path, path)
        
        if not file_path in self._cache:
            self._cache_path(file_path)
        
        digest = self._cache.get(file_path)
        
        if digest is None:
            return u'%s%s%s' % (
                self._host_url, 
                self._static_url_prefix, 
                path
            )
        else:
            return u'%s%s%s?v=%s' % (
                self._host_url, 
                self._static_url_prefix, 
                path, 
                digest[:snip_digest_at]
            )
        
    
    

