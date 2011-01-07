
==========
User Guide
==========

:ref:`weblayer` is made up of a number of components.  You can use it "out of the box", as shown by the :ref:`helloworld` example, or you can get stuck in under the hood and setup :ref:`weblayer` just the way you want, as explained in the :ref:`Components` section.

Once you have your application setup and configured the way you want it, you can write code that takes advantage of the :ref:`api`.


.. _helloworld:

Hello World
===========

`helloworld.py`_ shows how to start writing a web application using :ref:`weblayer`'s default configuration:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :linenos: 
   :lines: 7-

Let's walk through it.  First up, we import :py:class:`~weblayer.bootstrap.Bootstrapper`, :py:class:`~weblayer.request.RequestHandler` and :py:class:`~weblayer.wsgi.WSGIApplication`:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 7

Handling Requests
-----------------

We then see :py:class:`Hello`, a simple request handler (aka "view") that subclasses the :py:class:`~weblayer.request.RequestHandler` class we imported:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 9-13

:py:class:`Hello` has a single method defined called :py:meth:`get`.  This method will be called when :py:class:`Hello` receives an `HTTP GET request`_.

.. note::

    By default, request handlers accept GET and HEAD requests (i.e.: they are theoretically read only).  You can explicitly specify which methods of each request handler should be exposed using the :py:attr:`__all__` property.  For example, to handle GET, POST and DOFOO requests, you might write something like::

        class Hello2(RequestHandler):
            """ I explicitly accept only GET, POST and DOFOO requests.
            """
        
            __all__ = ('get', 'post', 'dofoo')
        
            def get(self):
                form = u'<form method="post"><input type="text" name="name" /></form>'
                return u'What is your name? %s' % form
        
            def post(self):
                return u'Hello %s!' % self.get_argument('name')
        
            def dofoo(self):
                return u'I just did foo!'
        
    

Handlers are mapped to incoming requests using the incoming request path.  This mapping takes the form of a list of tuples where the first item in the tuple is a `regular expression`_ and the second is a :py:class:`~weblayer.request.RequestHandler` class.

In this case, we map :py:class:`Hello` to all incoming requests:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 15

The `groups`_ in the regular expression (i.e.: the parts with parenthesis around them) that match the request path are passed to the appropriate method of the request handler as arguments.  So, in this case, an `HTTP GET request`_ to `/foo` will yield one match group, :py:obj:`'foo'` which is passed into :py:meth:`Hello.get` as the positional argument :py:obj:`world`, resulting in the response :py:obj:`u'hello foo'`.

You can see this for yourself by running::

    ./bin/weblayer-demo
    
And then opening http://localhost:8080/foo in a web browser.

.. note::

    The pattern of using an explicit, ordered mapping of regular expressions to request handlers is borrowed from (amongst others) Google App Engine's `webapp`_ framework.  Other patterns include `routes`_ and `traversal`_, sometimes used in tandem with `declarative configuration`_ and  / or `decorators`_.  
    
    :ref:`weblayer` avoids declarative configuration by default, largely to avoid imposing the overhead of learning and maintaining non-Python configuration files.  Decorators are not explicit and can introduce problems, as `explained here`_.
    
    Regular expressions are preferred over `routes`_ as they are both more powerful and an essential part of any Python developer's toolbox.  It seems strange to invent another tool for the job when the best one already exists.  Finally, `traversal`_ implies a context, which is overly prescriptive and not always the case.
    
    You may, of course, disagree with this analysis and :ref:`override <components>` the :py:class:`~weblayer.interfaces.IPathRouter` implementation as you see fit.

Required Settings
-----------------

With :ref:`weblayer`'s default configuration, you need to tell it where your static files and templates are and provide a secret string that your secure cookies are signed with so they can't be forged:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 17-21

You can explicitly require your own settings using a module level function call.  For example, the :py:attr:`cookie_secret` requirement is defined at the top of :py:mod:`weblayer.cookie` using:

.. literalinclude:: ../src/weblayer/cookie.py
   :lines: 26

See :py:mod:`weblayer.settings` for more details.

.. note::

    This pattern of optional explicit declaration of settings is borrowed from `tornado.options`_ and allows the application to throw an error on initialisation, rather than further down the line (e.g.: when a request happens to come in).
    
    :ref:`weblayer`'s implementation uses a `venusian scan`_ to prevent duplicate import issues.  This introduces a slight complexity: you must tell :ref:`weblayer` which modules or packages to scan for settings to be required.
    
    This can be done using the :py:obj:`packages` keyword argument when calling the :py:obj:`bootstrapper`, e.g.::
    
        settings, path_router = bootstrapper(packages=['your.package',])
    

Bootstrapping
-------------

:py:class:`~weblayer.bootstrap.Bootstrapper` is a helper class that simplifies component registration.  Here, we use it to bootstrap a :py:class:`~weblayer.wsgi.WSGIApplication` with some hardcoded application settings and the :ref:`url mapping` we defined above:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 23-24

.. note::

    The :py:class:`weblayer.bootstrap.Bootstrapper` is similar to `repoze.bfg's Configurator`_ in that it allows for imperative configuration of components.

Serving
-------

Finally, the remainder of the example takes care of serving the example application on http://localhost:8080:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 26-

For more realistic setups, see the :ref:`Deployment` recipes.


.. _components:

Components
==========

Architecture
------------

:ref:`weblayer` uses the `Zope Component Architecture <zope.component>`_ under the hood.  Individual components are said to `implement`_ one of :py:mod:`weblayer.interfaces`, listed in :py:obj:`weblayer.interfaces.__all__`:

.. literalinclude:: ../src/weblayer/interfaces.py
   :lines: 9-22

For example, :py:class:`~weblayer.route.RegExpPathRouter`::
    
    class RegExpPathRouter(object):
        """ Routes paths to request handlers using regexp patterns.
        """
        
        implements(IPathRouter)
        
        # `__init__` method removed from this example for brevity
        
        def match(self, path):
            """ Iterate through self._mapping.  If the path matches an item, 
              return the handler class, the `re` `match` object's groups (as args
              to pass to the handler) and an empty dict (as kwargs to pass to the
              handler).  Otherwise return `(None, None, None)`.
            """
            
            for regexp, handler_class in self._mapping:
                match = regexp.match(path)
                if match:
                    return handler_class, match.groups(), {}
                
            return None, None, None
            
        
    

Is one particular implementation of :py:class:`~weblayer.interfaces.IPathRouter`::

    class IPathRouter(Interface):
        """ Maps incoming requests to request handlers using the request path.
        """
        
        def match(path):
            """ Return `handler, args, kwargs` from `path`.
            """
            
        
    

Default Implementations
-----------------------

The default implementations are as follows:

* :py:class:`~weblayer.interfaces.IAuthenticationManager` is implemented by :py:class:`~weblayer.auth.TrivialAuthenticationManager`.
* :py:class:`~weblayer.interfaces.IMethodSelector` is implemented by :py:class:`~weblayer.method.ExposedMethodSelector`.
* :py:class:`~weblayer.interfaces.IPathRouter` is implemented by :py:class:`~weblayer.route.RegExpPathRouter`.
* :py:class:`~weblayer.interfaces.IRequest` is implemented by :py:class:`~weblayer.base.Request`.
* :py:class:`~weblayer.interfaces.IRequestHandler` is implemented by :py:class:`~weblayer.request.RequestHandler`.
* :py:class:`~weblayer.interfaces.IResponse` is implemented by :py:class:`~weblayer.base.Response`.
* :py:class:`~weblayer.interfaces.IResponseNormaliser` is implemented by :py:class:`~weblayer.response.DefaultToJSONResponseNormaliser`.
* :py:class:`~weblayer.interfaces.ISecureCookieWrapper` is implemented by :py:class:`~weblayer.cookie.SignedSecureCookieWrapper`.
* :py:class:`~weblayer.interfaces.ISettings` is implemented by :py:class:`~weblayer.settings.RequirableSettings`.
* :py:class:`~weblayer.interfaces.IStaticURLGenerator` is implemented by :py:class:`~weblayer.static.MemoryCachedStaticURLGenerator`.
* :py:class:`~weblayer.interfaces.ITemplateRenderer` is implemented by :py:class:`~weblayer.template.MakoTemplateRenderer`.
* :py:class:`~weblayer.interfaces.IWSGIApplication` is implemented by :py:class:`~weblayer.wsgi.WSGIApplication`.


Workflow
--------

Each application requires an :py:class:`~weblayer.interfaces.ISettings` implementation and an :py:class:`~weblayer.interfaces.IPathRouter`.  These are passed in to your :py:class:`~weblayer.interfaces.IWSGIApplication` when it is initialised, most commonly using the :py:class:`~weblayer.bootstrap.Bootstrapper`.

When HTTP requests come in to your application, :py:class:`~weblayer.interfaces.IWSGIApplication` uses the :py:class:`~weblayer.interfaces.IPathRouter` to map the incoming requests to an :py:class:`~weblayer.interfaces.IRequestHandler` that is instantiated with an :py:class:`~weblayer.interfaces.IRequest` that encapsulates the incoming request, a vanilla :py:class:`~weblayer.interfaces.IResponse` and the :py:class:`~weblayer.interfaces.ISettings`.

The :py:class:`~weblayer.interfaces.IRequestHandler` then uses the :py:class:`~weblayer.interfaces.IMethodSelector` to select a method (`def get()`, `def post()` etc.) to call to handle the request.  The method is then called with `*args` and `**kwargs` derived from the incoming request path by the :py:class:`~weblayer.interfaces.IPathRouter`.

When writing :py:class:`~weblayer.interfaces.IRequestHandler` code, you can access your :py:class:`~weblayer.interfaces.IStaticURLGenerator` at `self.static`, your :py:class:`~weblayer.interfaces.IAuthenticationManager` at `self.auth` and your :py:class:`~weblayer.interfaces.ISecureCookieWrapper` at `self.cookies`.  Your :py:class:`~weblayer.interfaces.ITemplateRenderer` is available through `self.render()`.
    
Finally, the return value of your handler method is passed to your :py:class:`~weblayer.interfaces.IResponseNormaliser`, which uses it to either replace or update the :py:class:`~weblayer.interfaces.IResponse` originally passed in to your :py:class:`~weblayer.interfaces.IRequestHandler` before the :py:class:`~weblayer.interfaces.IResponse` is returned as the response of your :py:class:`~weblayer.interfaces.IWSGIApplication`.


Overriding
----------

Alternative component implementations need to declare that they implement the appropriate interface and provide the attributes and methods that the interface specifies.  For example, an alternative  :py:class:`~weblayer.interfaces.IPathRouter` implementation needs to provide a :py:meth:`match` method, e.g.::

    class LazyPathRouter(object):
        """ Never even bothers trying.
        """
        
        implements(IPathRouter)
        
        def match(self, path):
            return None, None
        
    

The simplest way to then register this component is using the :py:class:`~weblayer.bootstrap.Bootstrapper` when bootstrapping the :py:class:`~weblayer.wsgi.WSGIApplication`.  The `override_path_router.py`_ example shows how:

.. literalinclude:: ../src/weblayer/examples/override_path_router.py
   :lines: 11-

If you then run this, all requests will meet with a 404 response::

    $ python src/weblayer/examples/override_path_router.py 
    ... "GET / HTTP/1.1" 404 0
    ... "GET /foo HTTP/1.1" 404 0


.. _api:

Request Handler API
===================

@@ ...

Request
-------

`self.request`

Response
--------

`self.response`

Settings
--------

`self.settings`

Arguments
---------

`self.get_argument(name, default=None, strip=False)`
`self.get_arguments(name, strip=False)`    

Authentication
--------------

`self.auth`

Secure Cookies
--------------

`self.cookies`

Templates
---------

`self.render(tmpl_name, **kwargs)`

Static URLs
-----------

`self.static`

XSRF
----

`self.xsrf_token`
`self.xsrf_input`

Redirection
-----------

`self.redirect(url, status=302, content_type=None)`

Errors
------

`self.error(status=500, body=u'System Error')`


.. _`helloworld.py`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/helloworld.py
.. _`override_path_router.py`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/override_path_router.py

.. _`HTTP GET request`: http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.3
.. _`regular expression`: http://docs.python.org/library/re.html
.. _`groups`: http://docs.python.org/library/re.html#re.MatchObject.groups

.. _`webapp`: http://code.google.com/appengine/docs/python/tools/webapp/
.. _`routes`: http://routes.groovie.org/
.. _`traversal`: http://docs.repoze.org/bfg/narr/traversal.html
.. _`declarative configuration`: http://docs.repoze.org/bfg/1.2/narr/configuration.html
.. _`decorators`: http://bottle.paws.de/docs/dev/tutorial.html#routing
.. _`explained here`: http://docs.repoze.org/bfg/current/designdefense.html#application-programmers-don-t-control-the-module-scope-codepath-import-time-side-effects-are-evil
.. _`tornado.options`: https://github.com/facebook/tornado/blob/master/tornado/options.py

.. _`venusian scan`: http://docs.repoze.org/venusian/
.. _`repoze.bfg's Configurator`: http://docs.repoze.org/bfg/narr/configuration.html
.. _`deployment`: recipes#deployment

.. _`implement`: http://pypi.python.org/pypi/zope.interface#declaring-implemented-interfaces
