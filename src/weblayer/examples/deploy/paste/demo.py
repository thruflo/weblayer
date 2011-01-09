#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" An example showing how to deploy `weblayer`_ using `Paste`_.
  
  .. _`weblayer`: http://packages.python.org/weblayer
  .. _`Paste`: http://pythonpaste.org/
"""

from weblayer import Bootstrapper, RequestHandler, WSGIApplication

class Hello(RequestHandler):
    def get(self, world):
        return u'hello %s' % world
    


# map urls to request handlers using regular expressions.
mapping = [(r'/(.*)', Hello)]

def app_factory(global_config, **local_conf):
    """ This function is defined as a `paste.app_factory` entry point in
      `./setup.py` and is called with configuration settings by::
      
          paster serve config.ini
      
    """
    
    # merge the global and local config
    config = global_config
    config.update(local_conf)
    
    # make `config['template_directories']` a list
    config['template_directories'] = [config['template_directory_path']]
    
    # instantiate the bootstrapper
    bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
    
    # return a bootstrapped `WSGIApplication`
    return WSGIApplication(*bootstrapper())
    

