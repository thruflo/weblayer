from thruflo.webapp.settings import require

@require('single_setting', category='thruflo.webapp.tests')
def foo(): # pragma: no cover
    pass
    

