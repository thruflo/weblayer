A minimal, testable WSGI framework::

    from thruflo.webapp import bootstrap, request, wsgi
    
    class Hello(request.Handler):
        @expose
        def get(self, world):
            return u'hello {}'.format(world)
        
    
    mapping = [(r'/(.*)', Hello)]
    
    def app_factory(global_config, **local_config):
        
        # parse paste config into one dict
        settings = global_config.copy()
        settings.update(local_config)
        
        # bootstrap component registrations
        bootstrapper = bootstrap.Bootstrapper(settings, url_mapping)
        bootstrapper.bootstrap()
        
        return wsgi.Application()
        
    
Run the tests::

    ./bin/nosetests -c etc/nose.cfg
    
Generate the docs::

    ./bin/sphinx-build -a -b html docs docs/_build
    
