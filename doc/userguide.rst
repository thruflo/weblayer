
==========
User Guide
==========


Hello World
===========

`helloworld.py`_ shows an example web application made using :ref:`weblayer`'s "out of the box" configuration:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :linenos: 
   :lines: 7-

Let's walk through it.  First up, the example shows three imports from :ref:`weblayer`:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 7

Request Handling
----------------

We then see :py:class:`Hello`, a simple request handler (also sometimes called a "view") that subclasses the :py:class:`weblayer.request.RequestHandler` class we imported:

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
                return u'What is your name? {}'.format(form)
        
            def post(self):
                return u'Hello {}!'.format(self.get_argument('name'))
        
            def dofoo(self):
                return u'I just did foo!'
        
    

URL Mapping
-----------

Handlers are mapped to incoming requests using the incoming request path.  This mapping takes the form of a list of tuples where the first item in the tuple is a `regular expression`_ and the second is a :py:class:`weblayer.request.RequestHandler` class.

In this case, we map :py:class:`Hello` to all incoming requests:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 15-16

The `groups`_ in the regular expression (i.e.: the parts with parenthesis around them) that match the request path are passed to the appropriate method of the request handler as arguments.  So, in this case, an `HTTP GET request`_ to `/foo` will yield one match group, :py:obj:`'foo'` which is passed into :py:meth:`Hello.get` as the positional argument :py:obj:`world`, resulting in the response :py:obj:`u'hello foo'`.

You can see this for yourself by running::

    ./bin/weblayer-demo
    
And then opening http://localhost:8080/foo in a web browser.

.. note::

    The pattern of using an explicit, ordered mapping of regular expressions to request handlers is borrowed from (amongst others) Google App Engine's `webapp`_ framework.  Other patterns include `routes`_ and `traversal`_, sometimes used in tandem with `declarative configuration`_ and  / or `decorators`_.  
    
    :ref:`weblayer` avoids declarative configuration by default, largely to avoid imposing the overhead of learning and maintaining non-Python configuration files.  Decorators are not explicit and can introduce problems, as `explained here`_.
    
    Regular expressions are preferred over `routes`_ as they are both more powerful and an essential part of any Python developer's toolbox.  It seems strange to invent another tool for the job when the best one already exists.  Finally, `traversal`_ implies a context, which is overly prescriptive and not always the case.
    
    You may, of course, disagree with this analysis and override the :py:class:`weblayer.interfaces.IPathRouter` implementation as you see fit.

Required Settings
-----------------

Carrying on through the example, we next define some required settings.  With :ref:`weblayer`'s default configuration, you need to tell it where your static files and templates are and provide a secret string that your secure cookies are signed with so they can't be forged:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 18-23

If you wish, you can explicitly require settings using a module level function call.  For example, the :py:attr:`cookie_secret` requirement is defined at the top of :py:mod:`weblayer.cookie` using:

.. literalinclude:: ../src/weblayer/cookie.py
   :lines: 26

See :py:mod:`weblayer.settings` for more details.

.. note::

    This pattern of optional explicit declaration of settings is borrowed from `tornado.options`_.  You can safely ignore it and make sure that you provide the settings your application requires.  However, explicitly requiring settings allows the application to throw an error on initialisation, rather than further down the line (e.g.: when a request to a specific handler happens to come in).
    
    :ref:`weblayer`'s implementation uses a `venusian scan`_ to prevent duplicate import issues.  This introduces a slight complexity: you must tell :ref:`weblayer` which modules or packages to scan for settings to be required.
    
    This can be done most simply using the :py:obj:`packages` keyword argument when calling the :py:obj:`bootstrapper` (introduced in the next section) e.g.::
    
        settings, path_router = bootstrapper(packages=['your.package',])
    


Bootstrapping
-------------

Next, we define an :py:func:`app_factory` function that returns a bootstrapped :py:class:`weblayer.wsgi.WSGIApplication`:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 25-28

:py:class:`weblayer.bootstrap.Bootstrapper` is a helper class that simplifies component registration.  You can use it "out of the box", as we do above, or you can use it to override specific components.

.. note::

    The :py:class:`weblayer.bootstrap.Bootstrapper` is similar to `repoze.bfg's Configurator`_ in that it allows for imperative configuration of components.

Serving
-------

Finally, the remainder of the example takes care of serving the example application on http://localhost:8080:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 31-

For more realistic setups, see the :ref:`Deployment` recipes.


Components
==========

@@ explain how it fits together and how to override
@@ n.b.: fix the refs in the other docs and in the docstrings...

.. _`helloworld.py`: https://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/helloworld.py

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
