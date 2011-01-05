
=======
Recipes
=======


Deployment
==========

Apache mod_wsgi
---------------

@@ ...

Appengine
---------

As a pure `Python`_ package, :ref:`weblayer` works perfectly on `Google App Engine`_, as shown by `./src/weblayer/examples/appengine`_.  The application is in `app.py`:

.. literalinclude:: ../src/weblayer/examples/appengine/app.py
   :lines: 24-

With the `App Engine configuration <http://code.google.com/appengine/docs/python/config/appconfig.html>`_ in `app.yaml` (you should replace `<<yourappid>>` with your application id):

.. literalinclude:: ../src/weblayer/examples/appengine/app.yaml

You can see this deployed at `http://weblayer-demo.appspot.com <http://weblayer-demo.appspot.com>`_.

.. note::

    You must have :ref:`weblayer` and its dependencies included your `Python Path`_, e.g.: by copying them into the same folder as `app.py` or by `amending sys.path`_.  Check the `install_requires` list in `setup.py`_ but at the time of writing this means you need to include:
    
    * `mako`, 
    * `venusian`, 
    * `weblayer`, 
    * `webob`, 
    * `zope.component`
    * `zope.interface`
    * `zope.event`
    * `pkg_resources.py`
    

Paste
-----

`weblayer`_ is WSGI compatible and so can be served using `Paste`_, as shown by `./src/weblayer/examples/paste`_.  The demo application is in `demo.py`:

.. literalinclude:: ../src/weblayer/examples/paste/demo.py
   :linenos: 
   :lines: 10-21,28-

`setup.py` defines a `weblayer-pastedemo` `Egg`_ with `demo.app_factory` as its main `paste.app_factory`_ entry point:

.. literalinclude:: ../src/weblayer/examples/paste/setup.py
   :linenos:

`config.ini` tells `Paste`_ to use the main entry point to the `weblayer-pastedemo` egg:

.. literalinclude:: ../src/weblayer/examples/paste/config.ini
   :linenos:

To run the example, develop the `weblayer-pastedemo` egg::

    cd ./src/weblayer/examples/paste
    python setup.py develop

Then use Paste Script's `paster serve`_ command::

    paster serve config.ini

.. note::
    
    The main difference between this and the `Hello World`_ example is the `demo.app_factory` function.  Notice that it accepts `global_config` and `local_config`:

    .. literalinclude:: ../src/weblayer/examples/paste/demo.py
       :lines: 21,28-

    `global_config` comes from the config file passed to `paster serve`, in this case `config.ini`.  `local_config` comes from the command line, e.g.::

        paster serve config.ini cookie_secret=blah
    


Buzzword Compliance
===================

Async / Non-blocking
--------------------

`weblayer`_ is agnostic as to whether it is served by a threaded, blocking server or an asynchronous, non-blocking one.  The simplest way to serve a non-blocking `weblayer`_ application is to deploy it behind `Gunicorn`_.

To use `weblayer`_ with `Gunicorn`_:

* see the `Gunicorn documentation`_ for information about installing, using, configuring and deploying it
* follow the instructions above on `Deploying with Paste`_
* amend your `[server:main]` section, as per `these instructions  <http://gunicorn.org/configure.html#paster-applications>`_, to include `use = egg:gunicorn#main`

For example, for a non-blocking server using `gevent`_ you might use the following configuration::

    [server:main]
    use = egg:gunicorn#main
    worker_class = gevent
    workers = 4
    host = 127.0.0.1
    port = 8080

Each request to your application will be handled in a `Greenlet <http://gunicorn.org/design.html#async-workers>`_.  This will be faster than a multi-threaded server if and only if your application is `IO bound <http://en.wikipedia.org/wiki/I/O_bound>`_.

Websockets
----------

The `websocket`_ specification is not yet fixed.  Different browsers implement different handshake procedures.  In December 2010, Firefox withdrew support for websockets, pending resolution of a security issue.

When these issues are resolved, it may be appropriate for `weblayer`_ to provide some sort of native web socket aware request handler.  Until then, simply use existing WSGI middleware, such as `gevent-websocket`_ and then look in `environ['wsgi.websocket']` or `environ['wsgi.input']` (or wherever the middleware sticks the reference to the socket) when writing request handler code, e.g.::

    class Echo(RequestHandler):
        """ Example websocket handler that echoes back any messages recieved.
        """
        
        def get(self):
            ws = self.request.environ['wsgi.websocket']
            while True:
                msg = ws.wait()
                if msg is None:
                    break
                ws.send(msg)
            
        
    



.. _`python`: #
.. _`weblayer`: #
.. _`google app engine`: #
.. _`app.yaml`: #
.. _`./src/weblayer/examples/paste`: #
.. _`./src/weblayer/examples/appengine`: #
.. _`egg`: #
.. _`paste.app_factory`: #
.. _`paster serve`: #
.. _`hello world`: #
.. _`gunicorn`: #
.. _`gunicorn documentation`: #
.. _`deploying with paste`: #
.. _`gevent`: #
.. _`websocket`: #
.. _`gevent-websocket`: #

.. _`Python Path`: http://code.google.com/appengine/docs/python/runtime.html
.. _`amending sys.path`: http://www.johnny-lin.com/cdat_tips/tips_pylang/path.html
.. _`setup.py`: http://github.com/thruflo/weblayer/tree/master/setup.py