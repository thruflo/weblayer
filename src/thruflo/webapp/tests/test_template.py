#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import unittest
from mock import Mock

from thruflo.webapp.template import MakoTemplateRenderer

class TestMakoTemplateRenderer(unittest.TestCase):
    """ Test the logic of the `MakoTemplateRenderer`.
    """
    
    def setUp(self):
        """
        """
        
        self.template_lookup_class = Mock()
        self.template_lookup_instance = Mock()
        self.template = Mock()
        self.template_lookup_class.return_value = self.template_lookup_instance
        self.template_lookup_instance.get_template.return_value = self.template
        self.template_renderer = MakoTemplateRenderer(
            directories=['a', 'b'],
            module_directory='c',
            built_ins={'d': 'e'},
            TemplateLookupClass=self.template_lookup_class,
            foo='bar'
        )
        
    
    def test_init_built_ins(self):
        """ `built_ins` are available as `self.built_ins` within
          the `MakoTemplateRenderer` instance.
        """
        
        self.assertTrue(self.template_renderer.built_ins == {'d': 'e'})
        
    
    def test_init_template_lookup(self):
        """ `TemplateLookupClass` is instantiated, passing through the
          appropriate parameters.
        """
        
        self.template_lookup_class.assert_called_with(
            directories=['a', 'b'],
            module_directory='c',
            input_encoding='utf-8',
            output_encoding='utf-8', 
            encoding_errors='replace',
            foo='bar'
        )
        
    
    def test_render_get_template(self):
        """ Calling `render(tmpl_name, ...)` on the `MakoTemplateRenderer` 
          instance calls get_template(tmpl_name) on the lookup instance. 
        """
        
        self.template_renderer.render('t')
        self.template_lookup_instance.get_template.assert_called_with('t')
        
    
    def test_render_template(self):
        """ Calling `render(tmpl_name, **kwargs)` calls template.render(), 
          passing through the `built_in`s, updated with the `kwargs`. 
        """
        
        self.template_renderer.render('foo.tmpl', baz='blah')
        self.template.render.assert_called_with(baz='blah', d='e')
        
    
    def test_render_template_kwargs_win(self):
        """ Where there's a clash, the `kwargs` win.
        """
        
        self.template_renderer.render('foo.tmpl', d='elephants')
        self.template.render.assert_called_with(d='elephants')
        
    
    


