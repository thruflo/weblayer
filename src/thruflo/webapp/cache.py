#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A Redis_ based cache. See ``RedisWrapper.__doc__``.
  
  .. _Redis: http://code.google.com/p/redis
"""

from redis import Redis as BaseRedis

from utils import url_escape

KEY_PREFIX = u'thruflo.'
EXPIRE_AFTER = 120 # seconds

class Redis(object):
    """Wraps a ``RedisClient`` instance with ``k`` -> 
      ``self._expand_redis_key(k)``.
      
          >>> redis = RedisWrapper(key_prefix='doc_tests')
          >>> 'a' in redis
          False
          >>> redis['a']
          >>> redis['a'] = 'a'
          >>> 'a' in redis
          True
          >>> redis['a']
          u'a'
          >>> del redis['a']
          >>> 'a' in redis
          False
      
      And ``__call__`` provides an all purpose workaround for 
      running any redis command, here we demo `ttl``::
          
          >>> import time
          >>> redis['a'] = 'a'
          >>> redis('ttl', 'a')
          120
          >>> time.sleep(2)
          >>> redis('ttl', 'a')
          118
      
      As you can see above, defaults every key to expire.  This is configurable
      as ``expire_after`` seconds::
          
          >>> redis = RedisWrapper(key_prefix='doc_tests', expire_after=60)
          >>> redis['a'] = 'a'
          >>> redis('ttl', 'a')
          60
      
      Clean up::
      
          >>> del redis['a']
      
    """
    
    def __init__(
            self, 
            db=0,
            namespace='',
            key_prefix=KEY_PREFIX, 
            expire_after=EXPIRE_AFTER
        ):
        self._r = BaseRedis(db=db)
        self.key_prefix = u'%s%s' % (key_prefix, namespace)
        self.expire_after = expire_after
        
    
    
    def _expand_redis_key(self, k):
        """Adds self.prefix to the start of all redis keys, to lower
          the risk of a namespace collision.
        """
        
        return u'%s%s' % (self.key_prefix, url_escape(k))
        
    
    
    def __contains__(self, k):
        k = self._expand_redis_key(k)
        return self._r.exists(k)
        
    
    def __getitem__(self, k):
        k = self._expand_redis_key(k)
        return self._r.get(k)
        
    
    def __setitem__(self, k, v):
        """We expire keys by default.  To work around this, use
          ``self.redis`` or ``self.set_and_expire``.
        """
        
        k = self._expand_redis_key(k)
        self._r.set(k, v)
        self._r.expire(k, self.expire_after)
        
    
    def __delitem__(self, k):
        k = self._expand_redis_key(k)
        return self._r.delete(k)
        
    
    
    def get(self, k, default=None):
        item = self[k]
        if item is not None:
            return item
        return default
    
    def set(self, k, v, delay=None, ts=None):
        """Set a key and expire after ``delay`` or at ``ts``.
        """
        
        k = self._expand_redis_key(k)
        self._r.set(k, v)
        if delay is not None:
            self._r.expire(k, delay)
        elif ts is not None:
            self._r.send_command(
                'EXPIREAT %s %s\r\n' % (
                    k,
                    ts
                )
            )
        
        
    
    
    def __call__(self, cmd, k, *args, **kwargs):
        """Passes any command through to the redis
        """
        
        method = getattr(self._r, cmd)
        if isinstance(k, list) or isinstance(k, tuple):
            k = [self._expand_redis_key(item) for item in k]
        else:
            k = self._expand_redis_key(k)
        return method(k, *args, **kwargs)
        
    
    
