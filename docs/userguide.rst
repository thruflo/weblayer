

User Guide
==========

Hello World
-----------

`helloworld.py`_ shows an example web application made using `weblayer`_'s default "out of the box" configuration:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :linenos: 

Let's walk through it.  First up, the example shows three imports from `weblayer`_:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 1

We then see `Hello`, a simple request handler class (also sometimes called a "view class") that subclasses the `RequestHandler`_ class we imported:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 3-7

`Hello` has a single method defined called `get`.  This method will be called when `Hello` receives an `HTTP GET request`_.

By default, request handlers accept GET and HEAD requests (i.e.: they are theoretically read only).  You can explicitly specify which methods of each request handler should be exposed using the `__all__` property.  For example, to handle GET, POST and DOFOO requests, you might write something like::

    class Hello2(RequestHandler):
        """ I explicitly accept only GET and POST requests.
        """
        
        __all__ = ('get', 'post', 'dofoo')
        
        def get(self):
            form = u'<form method="post"><input type="text" name="name" /></form>'
            return u'What is your name? {}'.format(form)
        
        def post(self):
            return u'Hello {}!'.format(self.get_argument('name'))
        
        def dofoo(self):
            return u'I just did foo!'
        
    

Handlers are mapped to incoming requests using the incoming request path.  This mapping takes the form of a list of tuples where the first item in the tuple is a `regular expression`_ and the second is a request handler class.

In this case, we map `Hello` to all incoming requests using the `regular expression`_ pattern `r'/(.*)'`:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 9-10

The groups in the regular expression (i.e.: the parts with parenthesis around them) that match the request path are passed to the appropriate method of the request handler as arguments.  So, in this case, an `HTTP GET request`_ to `/foo` will yield one match group, `'foo'` which is passed into `Hello.get` as the positional argument `world`, resulting in the response `u'hello foo'`.

You can see this for yourself by running::

    ./bin/weblayer-demo
    
And then opening http://localhost:8080/foo in a web browser.

Carrying on through the example, we next define some required settings:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 12-17

These are fairly self explanatory.  With `weblayer`_'s default configuration, you need to tell it where your static files and templates are and provide a secret string that your secure cookies are signed with so they can't be forged.




Deployment
----------

@@ deployment ...

* paste
* gunicorn
* mod_wsgi
* appengine


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
