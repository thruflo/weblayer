from weblayer.settings import require

@require('single_setting', category='weblayer.tests')
def foo(): # pragma: no cover
    pass
    

