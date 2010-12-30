#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weblayer.settings import require_setting, override

require_setting(
    'test_override_function', 
    default='something', 
    category='weblayer.tests'
)

@override(
    'test_override_function', 
    default='something else', 
    category='weblayer.tests'
)
def foo(): # pragma: no cover
    pass

