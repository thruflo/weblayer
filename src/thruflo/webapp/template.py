#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Mako boilerplate.
"""

import datetime

from os.path import dirname, join as join_path

from mako.template import Template
from mako.lookup import TemplateLookup

import utils

def tmpl_lookup_factory(tmpl_dirs):
    return TemplateLookup(
        directories=tmpl_dirs,
        module_directory='/tmp/mako_modules',
        input_encoding='utf-8', 
        output_encoding='utf-8', 
        encoding_errors='replace'
    )


builtin = {
    "escape": utils.xhtml_escape,
    "url_escape": utils.url_escape,
    "json_encode": utils.json_encode,
    "squeeze": utils.squeeze,
    "datetime": datetime,
}

def render_tmpl(tmpl_lookup, tmpl_name, **kwargs):
    t = tmpl_lookup.get_template(tmpl_name)
    kwargs.update(builtin)
    return t.render(**kwargs)
    

