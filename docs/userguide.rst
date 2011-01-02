
==========
User Guide
==========


Hello World
===========

`helloworld.py`_ shows an example web application made using `weblayer`_'s "out of the box" configuration:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :linenos: 
   :lines: 7-

Let's walk through it.  First up, the example shows three imports from `weblayer`_:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 7

Request Handling
----------------

We then see `Hello`, a simple request handler class (also sometimes called a "view class") that subclasses the `RequestHandler`_ class we imported:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 9-13

`Hello` has a single method defined called `get`.  This method will be called when `Hello` receives an `HTTP GET request`_.

.. note::

    By default, request handlers accept GET and HEAD requests (i.e.: they are theoretically read only).  You can explicitly specify which methods of each request handler should be exposed using the `__all__` property.  For example, to handle GET, POST and DOFOO requests, you might write something like::

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

Handlers are mapped to incoming requests using the incoming request path.  This mapping takes the form of a list of tuples where the first item in the tuple is a `regular expression`_ and the second is a request handler class.

In this case, we map `Hello` to all incoming requests:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 15-16

The groups in the regular expression (i.e.: the parts with parenthesis around them) that match the request path are passed to the appropriate method of the request handler as arguments.  So, in this case, an `HTTP GET request`_ to `/foo` will yield one match group, `'foo'` which is passed into `Hello.get` as the positional argument `world`, resulting in the response `u'hello foo'`.

You can see this for yourself by running::

    ./bin/weblayer-demo
    
And then opening http://localhost:8080/foo in a web browser.

.. note::

    The pattern of using an explicit, ordered mapping of regular expressions to request handlers is borrowed from (amongst others) Google App Engine's `webapp`_ framework.  The other popular patterns frameworks tend to use are `routes`_ and `traversal`_, sometimes used in tandem with `declarative configuration`_ or `decorators`_.  
    
    `weblayer`_ avoids declarative configuration by default, largely to avoid imposing the overhead of learning and maintaining non-Python configuration files.  Decorators are not explicit and can introduce problems, as `explained here`_.
    
    Regular expressions are preferred over `routes`_ as they are both more powerful and an essential part of any Python developer's toolbox.  It seems strange to invent another tool for the job when the best one already exists.  Finally, `traversal`_ implies a context, which is overly prescriptive and not always the case.
    
    You may, of course, disagree with this analysis and override the `Path Router component`_ as you see fit.

Settings
--------

Carrying on through the example, we next define some required settings.  With `weblayer`_'s default configuration, you need to tell it where your static files and templates are and provide a secret string that your secure cookies are signed with so they can't be forged:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 18-23

.. note::

    If you wish, you can explicitly require settings using a module level function call.  For example, the `cookie_secret` requirement is defined at the top of `weblayer.cookie`_ using:

    .. literalinclude:: ../src/weblayer/cookie.py
       :lines: 26

    This pattern of explicit declaration of settings is borrowed from `tornado.options`_.  It allows the application to throw an error on initialisation, rather than further down the line (e.g.: when a request to a specific handler happens to come in).
    
    `weblayer`_'s implementation is slightly different, using a `venusian scan`_ to prevent duplicate import issues.  This introduces a slight complexity: you must tell `weblayer`_ which modules or packages to scan for settings to be required.
    
    This can be done most simply using the `packages` keyword argument when calling the bootstrapper (introduced in the next section) e.g.::
    
        return WSGIApplication(*bootstrapper(packages=['your.package',]))
    
    See the `Settings component`_ and `Bootstrapper`_ for more details.

Bootstrapping
-------------

Next, we define an `app_factory` function that returns a bootstrapped `WSGIApplication`:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 25-28

`Bootstrapper`_ is a helper class that simplifies component registration.  You can use it "out of the box", as we do above, or you can use it to override specific components.

The `WSGIApplication`_ returned by the function uses a `Path Router`_ to match incoming requests to the appropriate request handler.

.. note::

    The `Bootstrapper` is similar to `repoze.bfg's Configurator`_ in that it allows for imperative configuration of components.

Serving
-------

Finally, the remainder of the example takes care of serving the example application on http://localhost:8080:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 31-

For more realistic setups, see the `Deployment`_ section.


Components
==========

Precursors
----------

Similar in utility to `weukzeug`_ while borrowing ideas from `repoze.bfg`_, `Tornado`_, `webapp`_ and `weblite`_,  to provide @@ ...

.. _`helloworld.py`: #
.. _`weblayer`: #

.. _`repoze.bfg`: #
.. _`Tornado`: #
.. _`webapp`: #
.. _`weblite`: #
.. _`weukzeug`: #
.. _`zope.component`: #

.. _`RequestHandler`: #
.. _`HTTP GET request`: #
.. _`regular expression`: #


.. _`routes`: #
.. _`traversal`: #
.. _`declarative configuration`: #
.. _`decorators`: #
.. _`explained here`: #
.. _`routes`: #
.. _`traversal`: #
.. _`requiring settings`: #
.. _`weblayer.cookie`: #
.. _`tornado.options`: #
.. _`path router component`: #

.. _`venusian scan`: #
.. _`settings component`: #
.. _`bootstrapper`: #
.. _`wsgiapplication`: #
.. _`path router`: #
.. _`repoze.bfg's Configurator`: #
.. _`deployment`: #
