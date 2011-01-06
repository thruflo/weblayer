from weblayer.settings import require, require_setting
from weblayer.settings import override, override_setting

require_setting('test_module', category='weblayer.tests')

@require('test_function', category='weblayer.tests')
def foo(): # pragma: no cover
    pass


class Foo(object):
    @require('test_method', category='weblayer.tests')
    def bar(self): # pragma: no cover
        pass
    

