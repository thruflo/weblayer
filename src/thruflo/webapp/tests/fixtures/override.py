#!/usr/bin/env python
# -*- coding: utf-8 -*-

from thruflo.webapp.settings import require_setting, override

require_setting(
    'test_override_function', 
    default='something', 
    category='thruflo.webapp.tests'
)

@override(
    'test_override_function', 
    default='something else', 
    category='thruflo.webapp.tests'
)
def foo(): # pragma: no cover
    pass

