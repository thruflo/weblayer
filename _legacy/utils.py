#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Shared helper functions.
"""

import logging
import hashlib
import random
import re
import time
import urllib
import xml.sax.saxutils

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        try:
            from django.utils import simplejson as json
        except ImportError:
            raise ImportError("A JSON parser is required")
        
    

def utf8(value):
    if isinstance(value, unicode):
        return value.encode("utf-8")
    assert isinstance(value, str)
    return value

def _unicode(value):
    if isinstance(value, str):
        return value.decode("utf-8")
    assert isinstance(value, unicode)
    return value


def unicode_urlencode(params):
    if isinstance(params, dict):
        params = params.items()
    return urllib.urlencode([(
                k, 
                isinstance(v, unicode) and v.encode('utf-8') or v
            ) for k, v in params
        ]
    )


def generate_hash(algorithm='sha1', s=None):
    """Generates a random string.
    """
    
    # if a string has been provided use it, otherwise default 
    # to producing a random string
    s = s is None and '%s%s' % (random.random(), time.time()) or s
    hasher = getattr(hashlib, algorithm)
    return hasher(s).hexdigest()
    


def json_encode(value, ensure_ascii=False, **kwargs):
    """JSON-encodes the given Python object."""
    
    return json.dumps(value, ensure_ascii=ensure_ascii, **kwargs)
    

def json_decode(value, **kwargs):
    """Returns Python objects for the given JSON string."""
    
    return json.loads(_unicode(value), **kwargs)
    


def get_timezones():
    """Returns a list of tuples, ordered by offset::
        
        >>> get_timezones()
        [(u'-11:00', u'Nome'), (u'-11:00', u'Atka'), ...
        ... (u'+10:00', u'Victoria'), (u'+11:00', u'Anadyr')]
    """
    
    results = []
    data = []
    
    for item in pytz.common_timezones:
        offset = pytz.timezone(item)._utcoffset
        hours = offset.seconds / 3600
        if hours > 12:
            hours = 0 - int(24 - hours)
        s = unicode(hours)
        if not s.startswith(u'-'):
            s = u'+%s' % s
        s = s[:3]
        if len(s) < 3:
            s = u'%s0%s' % (s[0], s[1])
        data.append((
                u'%s:00' % s, 
                u'/' in item and item.split(u'/')[1] or item
            )
        )
    
    for item in sorted(data):
        if item[0].startswith(u'-'):
            results.append(item)
        
    results.reverse()
    
    for item in sorted(data):
        if item[0].startswith(u'+'):
            results.append(item)
        
    return results
    


def xhtml_escape(value):
    """Escapes a string so it is valid within XML or XHTML.
    """
    
    return utf8(xml.sax.saxutils.escape(value, {'"': "&quot;"}))
    

def squeeze(value):
    """Replace all sequences of whitespace chars with a single space.
    """
    
    return re.sub(r"[\x00-\x20]+", " ", value).strip()
    

def url_escape(value):
    """Returns a valid URL-encoded version of the given value.
    """
    
    return urllib.quote_plus(utf8(value))
    

