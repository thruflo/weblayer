#!/usr/bin/env python
# -*- coding: utf-8 -*-

from thruflo.webapp.settings import override

@override('test_override_function', default='something else')
def foo(): # pragma: no cover
    pass

