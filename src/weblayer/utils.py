#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" :py:mod:`weblayer.utils` provides a set of utility functions for
  converting and encoding.
"""

__all__ = [
    'encode_to_utf8',
    'decode_to_unicode',
    'xhtml_escape',
    'url_escape',
    'unicode_urlencode',
    'json_encode',
    'json_decode',
    'generate_hash'
]

import hashlib
import random
import time
import urllib
import xml.sax.saxutils

try: #pragma NO COVERAGE
    import simplejson as json
except ImportError: #pragma NO COVERAGE
    import json

def encode_to_utf8(value):
    """ Converts a ``unicode`` to a utf-8 encoded ``str``::
      
          >>> a = u'foo'
          >>> a
          u'foo'
          >>> encode_to_utf8(a)
          'foo'
          >>> b = u'\u817e\u8baf\u9996\u9875'
          >>> c = '\xe8\x85\xbe\xe8\xae\xaf\xe9\xa6\x96\xe9\xa1\xb5'
          >>> assert encode_to_utf8(b) == c
      
      Regular strings get left alone::
      
          >>> d = 'foo'
          >>> encode_to_utf8(d)
          'foo'
      
      Other types raise a ``ValueError``::
      
          >>> e = None
          >>> encode_to_utf8(e) #doctest: +NORMALIZE_WHITESPACE
          Traceback (most recent call last):
          ...
          ValueError: None must be a `basestring`
      
    """
    
    if not isinstance(value, basestring):
        raise ValueError('%s must be a `basestring`' % value)
    elif isinstance(value, unicode):
        return value.encode("utf-8")
    return value
    

def decode_to_unicode(value):
    """ Converts a (hopefully) utf-8 encoded ``str`` to a ``unicode``::
      
          >>> a = 'foo'
          >>> decode_to_unicode(a)
          u'foo'
          >>> b = '\xe8\x85\xbe\xe8\xae\xaf\xe9\xa6\x96\xe9\xa1\xb5'
          >>> decode_to_unicode(b)
          u'\u817e\u8baf\u9996\u9875'
      
      Unicode values get left alone::
      
          >>> c = u'foo'
          >>> decode_to_unicode(c)
          u'foo'
      
      Other types raise a ``ValueError``::
      
          >>> d = None
          >>> decode_to_unicode(d) #doctest: +NORMALIZE_WHITESPACE
          Traceback (most recent call last):
          ...
          ValueError: None must be a `basestring`
      
    """
    
    if not isinstance(value, basestring):
        raise ValueError('%s must be a `basestring`' % value)
    elif isinstance(value, str):
        return value.decode("utf-8")
    return value
    

def unicode_urlencode(items):
    """ Ensures all ``items`` are encoded to utf-8 and passed to
      :py:func:`~urllib.urlencode`.
      
      Pass it a dict, comes out like a query string::
      
          >>> r1 = unicode_urlencode({'a': 'b'})
          >>> r1
          'a=b'
      
      Ditto a list of two item tuples::
      
          >>> r2 = unicode_urlencode([('a', 'b')])
          >>> r2 == r1
          True
      
      Converting any unicode values to utf8::
      
          >>> unicode_urlencode({'a': u'b'})
          'a=b'
          >>> r3 = unicode_urlencode({'a': u'\u817e\u8baf\u9996\u9875'})
          >>> r3
          'a=%E8%85%BE%E8%AE%AF%E9%A6%96%E9%A1%B5'
      
      Before running them through :py:func:`~urllib.urlencode`::
      
          >>> from urllib import urlencode
          >>> r4 = urlencode({'a': encode_to_utf8(u'\u817e\u8baf\u9996\u9875')})
          >>> r4 == r3
          True
      
      All values must be instances of ``basestring``::
      
          >>> unicode_urlencode({'a': object()}) #doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
          Traceback (most recent call last):
          ...
          ValueError: <object object ... must be a `basestring`
      
      Lists must contain at least two values to unpack::
      
          >>> unicode_urlencode(['a', 'b']) #doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
          Traceback (most recent call last):
          ...
          ValueError: need more than 1 value to unpack
      
      And not more than two values to unpack::
      
          >>> unicode_urlencode([('a', 'b', 'c')]) #doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
          Traceback (most recent call last):
          ...
          ValueError: too many values to unpack
      
    """
    
    if isinstance(items, dict):
        items = items.items()
    items = [(k, encode_to_utf8(v)) for k, v in items]
    return urllib.urlencode(items)
    


def xhtml_escape(value):
    """Escapes a string so it is valid within XML or XHTML::
      
          >>> xhtml_escape('a')
          'a'
          >>> xhtml_escape('<')
          '&lt;'
          >>> xhtml_escape('&')
          '&amp;'
      
      Including double quotes::
      
          >>> xhtml_escape('"')
          '&quot;'
      
      Encoding the result to utf-8::
      
          >>> xhtml_escape(u'a')
          'a'
      
    """
    
    escaped = xml.sax.saxutils.escape(value, {'"': "&quot;"})
    return encode_to_utf8(escaped)
    

def url_escape(value):
    """ Returns a URL-encoded version of ``value``.
      
      Runs the value through :py:func:`~urllib.quote_plus`::
      
          >>> url_escape('a')
          'a'
          >>> url_escape(' ')
          '+'
          
      Encoding it first to utf-8::
      
          >>> url_escape(u'a')
          'a'
          >>> url_escape(u'http://foo.com?bar=baz')
          'http%3A%2F%2Ffoo.com%3Fbar%3Dbaz'
      
      Which means the value must be a ``basestring``::
      
          >>> url_escape(None) #doctest: +ELLIPSIS
          Traceback (most recent call last):
          ...
          ValueError: None must be a `basestring`
      
    """
    
    return urllib.quote_plus(encode_to_utf8(value))
    


def json_encode(value, ensure_ascii=False, **kwargs):
    """ JSON encodes the given ``value``::
      
          >>> json_encode({'a': 'b'}) == json.dumps({'a': 'b'})
          True
          >>> json_encode({'a': 'b'})
          '{"a": "b"}'
          >>> json_encode({'a': None})
          '{"a": null}'
          >>> json_encode([])
          '[]'
          
      With ``ensure_ascii`` ``False`` by default::
      
          >>> json_encode({'a': u'\u817e\u8baf\u9996\u9875'})
          u'{"a": "\u817e\u8baf\u9996\u9875"}'
          >>> result = json_encode({'a': u'\u817e\u8baf'}, ensure_ascii=True)
          >>> result == '{"a": "\\u817e\\u8baf"}'
          True
      
      Raises a ``TypeError`` if the ``value`` isn't serializable::
      
          >>> json_encode([object()]) #doctest: +ELLIPSIS
          Traceback (most recent call last):
          ...
          TypeError: <object object ... is not JSON serializable
      
    """
    
    return json.dumps(value, ensure_ascii=ensure_ascii, **kwargs)
    

def json_decode(value, **kwargs):
    """ If ``value`` is valid JSON, parses it into a Python object::
      
          >>> json_decode('{}') == json.loads('{}')
          True
          >>> json_decode('{}')
          {}
          >>> json_decode('[null]')
          [None]
      
      Passing the value through :py:func:`decode_to_unicode` to start with::
      
          >>> json_decode('{"a": "b"}')
          {u'a': u'b'}
          >>> json_decode('{"a": "\\u817e\\u8baf\\u9996\\u9875"}')
          {u'a': u'\u817e\u8baf\u9996\u9875'}
      
      Raises a ``ValueError`` if the decoded ``value`` can't be parsed::
      
          >>> json_decode('{"a": object()}') #doctest: +ELLIPSIS
          Traceback (most recent call last):
          ...
          ValueError: No JSON object could be decoded
      
    """
    
    return json.loads(decode_to_unicode(value), **kwargs)
    


def generate_hash(algorithm='sha512', s=None, block_size=512):
    """ Generates a :py:func:`~hashlib.hash.hexdigest` string, either randomly
      or from a string or file like object (like an open file or a buffer).
      
      By default, the hash is randomly generated and uses the ``sha512``
      algorithm::
      
          >>> s1 = generate_hash()
          >>> isinstance(s1, str)
          True
          >>> len(s1) == 128
          True
          >>> s2 = generate_hash()
          >>> s1 == s2
          False
          >>> s3 = generate_hash(algorithm='sha512')
          >>> len(s1) == len(s3)
          True
      
      The hash can be generated from a seed::
      
          >>> generate_hash(s='a')
          '1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f5302860c652bf08d560252aa5e74210546f369fbbbce8c12cfc7957b2652fe9a75'
      
      Using ``None`` as the seed (which is the default) will, as we've seen, 
      generate a random value::
      
          >>> s6 = generate_hash(s=None)
          >>> s7 = generate_hash(s=None)
          >>> s6 == s7
          False
      
      Using a file like object (anything with a ``read()`` method) will use
      the contents of the file like object::
      
          >>> from StringIO import StringIO
          >>> sock = StringIO()
          >>> sock.write('abc')
          >>> sock.seek(0)
          >>> s8 = generate_hash(s=sock)
          >>> s9 = generate_hash(s='abc')
          >>> s8 == s9
          True
      
      Reading the contents into memory in blocks of ``block_size``, which
      defaults to ``512``::
      
          >>> from mock import Mock
          >>> sock = Mock()
          >>> sock.read.return_value = None
          >>> s10 = generate_hash(s=sock)
          >>> sock.read.assert_called_with(512)
          >>> s10 = generate_hash(s=sock, block_size=1024)
          >>> sock.read.assert_called_with(1024)
      
      Using other types as a seed (anything that :py:mod:`hashlib` doesn't
      like) will raise a ``TypeError``::
      
          >>> generate_hash(s=[]) #doctest: +ELLIPSIS
          Traceback (most recent call last):
          ...
          TypeError: ...
      
      The algorithm name can also be passed in::
      
          >>> s4 = generate_hash(algorithm='md5')
          >>> s5 = generate_hash(algorithm='sha224')
          >>> len(s4) == 32 and len(s5) == 56
          True
      
      As long as it's available in :py:mod:`hashlib`::
      
          >>> generate_hash(algorithm='foo')
          Traceback (most recent call last):
          ...
          AttributeError: 'module' object has no attribute 'foo'
      
    """
    
    # get the hasher
    hasher = getattr(hashlib, algorithm)()
    
    # read in the data
    if hasattr(s, 'read') and callable(s.read):
        while True:
            data = s.read(block_size)
            if not data:
                break
            hasher.update(data)
    else:
        if s is None:
            s = '%s%s' % (random.random(), time.time())
        hasher.update(s)
    
    # return a hexdigest of the hash
    return hasher.hexdigest()
    

