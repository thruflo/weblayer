from thruflo.webapp.settings import require, require_setting
from thruflo.webapp.settings import override, override_setting

require_setting('test_module', category='thruflo.webapp.tests')

@require('test_function', category='thruflo.webapp.tests')
def foo(): # pragma: no cover
    pass


@require('test_class', category='thruflo.webapp.tests')
class Foo(object):
    @require('test_method', category='thruflo.webapp.tests')
    def bar(self): # pragma: no cover
        pass
    

