Yet another WSGI layer::

    from thruflo.webapp import Bootstrapper, RequestHandler, WSGIApplication
    from thruflo.webapp.method import expose
    
    class Hello(RequestHandler):
        @expose
        def get(self, world):
            return u'hello {}'.format(world)
            
        
    
    url_mapping = [(r'/(.*)', Hello)]
    app_settings = {
        'cookie_secret', '...',
        'static_files_path': '/var/www/static',
        'template_directories': ['/my/app/templates']
    }
    
    bootstrapper = Bootstrapper(app_settings, url_mapping)
    application = WSGIApplication(**bootstrapper())
    
    if __name__ == '__main__':
        from paste.httpserver import serve
        serve(application)
        
    

Run the tests::

    ./bin/nosetests -c etc/nose.cfg
    
Generate the docs::

    ./bin/sphinx-build -a -b html docs docs/_build
    
