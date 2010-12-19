#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Expand and cache static urls.
"""

__all__ = [
    'MemoryCachedStaticURLGenerator'
]

from os.path import join

from zope.component import adapts
from zope.interface import implements

from interfaces import IRequest, IRequirableSettings, IStaticURLGenerator
from settings import require_setting
from utils import generate_hash

require_setting('static_path', default=u'/var/www/static')
require_setting('static_url_prefix', default=u'/static/')

class MemoryCachedStaticURLGenerator(object):
    """ Adapter to generate static URLs from a request.
    """
    
    _cache = {}
    
    adapts(IRequest, IRequirableSettings)
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
              >>> settings['static_path'] = '/var/www/static'
              >>> settings['static_url_prefix'] = u'/static/'
              >>> static = MemoryCachedStaticURLGenerator(
              ...     req, 
              ...     settings
              ... )
              >>> static._host_url
              'foo.com'
          
          `settings['static_path']` and `settings['static_url_prefix']` are
          available as `self._static_path` and `self._static_url_prefix`::
          
              >>> static = MemoryCachedStaticURLGenerator(
              ...     req, 
              ...     settings
              ... )
              >>> static._static_path
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
        self._static_path = settings['static_path']
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
        """
        
        file_path = self._join_path(self._static_path, path)
        try:
            sock = self._open_file(file_path)
        except IOError:
            logging.warning(u'Couldn\'t open static file {}'.format(file_path))
            self._cache[path] = None
        else:
            digest = self._generate_hash(s=sock)
            sock.close()
            self._cache[path] = digest
        
    
    def get_url(self, path, snip_digest_at=7):
        """ Get a fully expanded url for the given static resource `path`.
        """
        
        if not path in self._cache:
            self._cache_path(path)
        
        digest = self._cache.get(path)
        
        if digest is None:
            return u'{}{}{}'.format(
                self._host_url, 
                self._static_url_prefix, 
                path
            )
        else:
            return u'{}{}{}?v={}'.format(
                self._host_url, 
                self._static_url_prefix, 
                path, 
                digest[:snip_digest_at]
            )
        
    
    

