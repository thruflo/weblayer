#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Notes:
  
  - we want to use paste's parsing, so settings need to get
    setup in, e.g.: `Bootstrapper().set_settings(settings)`
  - settings could then we available via a simple 
    `getUtility(ISettings)`
  
  - however, `define()` is also a nice pattern to declare 
    required settings -- or is it?  do we just simple use
    an interface?  or do we make it a decorator?
  - perhaps if we do `define` we could then add the module
    name as a path, e.g.: `settings.template.directories`
  
"""

