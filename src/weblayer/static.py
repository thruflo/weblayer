#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Expand and cache static urls.
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
        
    
    def _cache_path(self, path):
        """ Expand the request `path` into a `file_path`, check to see if
          it exists, if it does, hash it and store the `digest` against
          the `path` in the `_cache`.
          
              >>> from mock import Mock
              >>> from StringIO import StringIO
              >>> request = Mock()
              >>> join_path = Mock()
              >>> join_path.return_value = '/var/www/static/foo.js'
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
              ...     join_path_=join_path,
              ...     open_file_=open_file,
              ...     generate_hash_=generate_hash
              ... )
              >>> static._cache_path('/foo.js')
          
          `path` is expanded into `file_path` by `join_path`::
          
              >>> join_path.assert_called_with('/var/www/static', '/foo.js')
          
          If `file_path` exists::
          
              >>> open_file.assert_called_with('/var/www/static/foo.js')
          
          It's hashed::
          
              >>> generate_hash.assert_called_with(s=sock)
          
          The hash is cached::
          
              >>> static._cache['/foo.js']
              'digest'
          
          Unless the file_path can't be opened::
          
              >>> def open_file(file_path):
              ...     raise IOError
              ... 
              >>> static = MemoryCachedStaticURLGenerator(
              ...     request, 
              ...     settings,
              ...     join_path_=join_path,
              ...     open_file_=open_file,
              ...     generate_hash_=generate_hash
              ... )
              >>> static._cache_path('/foo.js')
              >>> static._cache['/foo.js'] is None
              True
          
        """
        
        file_path = self._join_path(self._static_files_path, path)
        try:
            sock = self._open_file(file_path)
        except IOError:
            logging.warning(u'Couldn\'t open static file %s' % file_path)
            self._cache[path] = None
        else:
            digest = self._generate_hash(s=sock)
            sock.close()
            self._cache[path] = digest
        
    
    def get_url(self, path, snip_digest_at=7):
        """ Get a fully expanded url for the given static resource `path`::
          
              >>> from mock import Mock
              >>> request = Mock()
              >>> request.host_url = 'http://static.foo.com'
              >>> settings = {}
              >>> settings['static_files_path'] = '/var/www/static'
              >>> settings['static_url_prefix'] = u'/static/'
              >>> MemoryCachedStaticURLGenerator._cache = {}
              >>> static = MemoryCachedStaticURLGenerator(
              ...     request, 
              ...     settings
              ... )
              >>> static._cache_path = Mock()
          
          If `path` isn't in `self._cache`, calls `self._cache_path(path)`::
          
              >>> url = static.get_url('foo')
              >>> static._cache_path.assert_called_with('foo')
          
          If the digest is `None`, just joins the host url, prefix and path::
          
              >>> static._cache['foo'] = None
              >>> static.get_url('foo')
              u'http://static.foo.com/static/foo'
          
          Else also appends `?v=' plus upto the first `snip_digest_at` chars 
          of the digest, which defaults to `7`::
          
              >>> static._cache['foo'] = 'abcdefghijkl'
              >>> static.get_url('foo', snip_digest_at=4)
              u'http://static.foo.com/static/foo?v=abcd'
              >>> static.get_url('foo')
              u'http://static.foo.com/static/foo?v=abcdefg'
          
        """
        
        if not path in self._cache:
            self._cache_path(path)
        
        digest = self._cache.get(path)
        
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
        
    
    

