#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for `weblayer.template`.
"""

import unittest
from mock import Mock

class TestMakoTemplateRenderer(unittest.TestCase):
    """ Test the logic of the `MakoTemplateRenderer`.
    """
    
    def setUp(self):
        self.settings = {'template_directories': ['a', 'b']}
        self.template_lookup_class = Mock()
        self.template_lookup_instance = Mock()
        self.template = Mock()
        self.template_lookup_class.return_value = self.template_lookup_instance
        self.template_lookup_instance.get_template.return_value = self.template
        
    
    def make_one(self, *args, **kwargs):
        from weblayer.template import MakoTemplateRenderer
        return MakoTemplateRenderer(*args, **kwargs)
        
    
    def test_init_built_ins(self):
        """ `built_ins` are available as `self.built_ins` within
          the `MakoTemplateRenderer` instance.
        """
        
        template_renderer = self.make_one(
            self.settings,
            module_directory='c',
            built_ins={'d': 'e'},
            template_lookup_class=self.template_lookup_class,
            foo='bar'
        )
        
        self.assertTrue(template_renderer.built_ins == {'d': 'e'})
        
    
    def test_init_template_lookup(self):
        """ `TemplateLookupClass` is instantiated, passing through the
          appropriate parameters.
        """
        
        template_renderer = self.make_one(
            self.settings,
            module_directory='c',
            built_ins={'d': 'e'},
            template_lookup_class=self.template_lookup_class,
            foo='bar'
        )
        
        self.template_lookup_class.assert_called_with(
            directories=['a', 'b'],
            module_directory='c',
            input_encoding='utf-8',
            output_encoding='utf-8', 
            encoding_errors='replace',
            foo='bar'
        )
        
    
    def test_init_template_lookup_none(self):
        """ Uses `template.TemplateLookup` as default `template_lookup_class`.
        """
        
        from weblayer import template
        __TemplateLookup = template.TemplateLookup
        TemplateLookup = Mock()
        template.TemplateLookup = TemplateLookup
        
        template_renderer = self.make_one(
            self.settings,
            module_directory='c',
            built_ins={'d': 'e'},
            template_lookup_class=None,
            foo='bar'
        )
        
        TemplateLookup.assert_called_with(
            directories=['a', 'b'],
            module_directory='c',
            input_encoding='utf-8',
            output_encoding='utf-8', 
            encoding_errors='replace',
            foo='bar'
        )
        
        template.TemplateLookup = __TemplateLookup
        
    
    def test_render_get_template(self):
        """ Calling `render(tmpl_name, ...)` on the `MakoTemplateRenderer` 
          instance calls get_template(tmpl_name) on the lookup instance. 
        """
        
        template_renderer = self.make_one(
            self.settings,
            module_directory='c',
            built_ins={'d': 'e'},
            template_lookup_class=self.template_lookup_class,
            foo='bar'
        )
        template_renderer.render('t')
        self.template_lookup_instance.get_template.assert_called_with('t')
        
    
    def test_render_template(self):
        """ Calling `render(tmpl_name, **kwargs)` calls template.render(), 
          passing through the `built_in`s, updated with the `kwargs`. 
        """
        
        template_renderer = self.make_one(
            self.settings,
            module_directory='c',
            built_ins={'d': 'e'},
            template_lookup_class=self.template_lookup_class,
            foo='bar'
        )
        template_renderer.render('foo.tmpl', baz='blah')
        self.template.render.assert_called_with(baz='blah', d='e')
        
    
    def test_render_template_kwargs_win(self):
        """ Where there's a clash, the `kwargs` win.
        """
        
        template_renderer = self.make_one(
            self.settings,
            module_directory='c',
            built_ins={'d': 'e'},
            template_lookup_class=self.template_lookup_class,
            foo='bar'
        )
        template_renderer.render('foo.tmpl', d='elephants')
        self.template.render.assert_called_with(d='elephants')
        
    
    


