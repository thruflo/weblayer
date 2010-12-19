A minimal, testable WSGI framework::

    from thruflo.webapp import Bootstrapper, RequestHandler, WSGIApplication
    from thruflo.webapp.method import expose
    
    class Hello(RequestHandler):
        @expose
        def get(self, world):
            return u'hello {}'.format(world)
        
    
    url_mapping = [(r'/(.*)', Hello)]
    
    app_settings = {
        'cookie_secret', u'...',
        'static_path': u'/var/www/static',
        'static_url_prefix', u'/static/',
        'template_directories': '/foo/bar/templates'
    }
    
    if __name__ == '__main__':
        bootstrapper = Bootstrapper(app_settings, url_mapping)
        settings, path_router = bootstrapper.bootstrap()
        application = WSGIApplication(settings, path_router)
        
        from paste.httpserver import serve
        serve(application, host='0.0.0.0')
    
Run the tests::

    ./bin/nosetests -c etc/nose.cfg
    
Generate the docs::

    ./bin/sphinx-build -a -b html docs docs/_build
    
