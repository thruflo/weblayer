
=======
Recipes
=======

.. _deployment:

Deployment
==========

Apache mod_wsgi
---------------

:ref:`weblayer` is `WSGI`_ compatible and so can be served using `Apache mod_wsgi`_.  By default, `Apache mod_wsgi`_ looks for a callable entry point called :py:obj:`application` in an application script file (essentially a `Python`_ module saved with a `.wsgi` extension).

In our example, `./src/weblayer/examples/deploy/mod_wsgi`_, the application script file is `app.wsgi`:

.. literalinclude:: ../src/weblayer/examples/deploy/mod_wsgi/app.wsgi
   :lines: 20-

This is then hooked up in `your apache configuration`_ using the `WSGIScriptAlias directive`_, e.g.::

    WSGIScriptAlias / /path/to/app.wsgi

Appengine
---------

As a pure `Python`_ package that's compatible with Python 2.5, :ref:`weblayer` works perfectly on `Google App Engine`_.  In our example, `./src/weblayer/examples/deploy/appengine`_, the application is in `app.py`:

.. literalinclude:: ../src/weblayer/examples/deploy/appengine/app.py
   :lines: 24-

With the `App Engine configuration <http://code.google.com/appengine/docs/python/config/appconfig.html>`_ in `app.yaml` (you should replace `weblayer-demo` with your application id):

.. literalinclude:: ../src/weblayer/examples/deploy/appengine/app.yaml

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

:ref:`weblayer` is `WSGI`_ compatible and so can be served using `Paste`_, as shown by `./src/weblayer/examples/deploy/paste`_.  The demo application is in `demo.py`:

.. literalinclude:: ../src/weblayer/examples/deploy/paste/demo.py
   :lines: 10-21,28-

`setup.py` defines a `weblayer-pastedemo` `Egg`_ with :py:func:`demo.app_factory` as its main `paste.app_factory`_ entry point:

.. literalinclude:: ../src/weblayer/examples/deploy/paste/setup.py

`config.ini` tells `Paste`_ to use the main entry point to the `weblayer-pastedemo` egg:

.. literalinclude:: ../src/weblayer/examples/deploy/paste/config.ini

To run the example, develop the `weblayer-pastedemo` egg::

    cd ./src/weblayer/examples/paste
    python setup.py develop

Then use Paste Script's `paster serve`_ command::

    paster serve config.ini

.. note::
    
    The main difference between this and the :ref:`Hello World` example is the :py:func:`demo.app_factory` function.  Notice that it accepts :py:obj:`global_config` and :py:obj:`local_config`:

    .. literalinclude:: ../src/weblayer/examples/deploy/paste/demo.py
       :lines: 21,28-

    :py:obj:`global_config` comes from the config file passed to `paster serve`, in this case `config.ini`.  :py:obj:`local_config` comes from the command line, e.g.::

        paster serve config.ini cookie_secret=blah
    
.. note::
    
    All `Paste config values`_ are strings.  If you want other types as your settings values, you will need to parse the config values yourself (i.e.: it is outside the scope of :ref:`weblayer`).  We illustrate this trivially in the example by parsing the `template_directory_path` string into the `template_directories` list required by :py:mod:`weblayer.template`:
    
    .. literalinclude:: ../src/weblayer/examples/deploy/paste/demo.py
       :lines: 33-34
    


Buzzword Compliance
===================

Async / Non-blocking
--------------------

:ref:`weblayer` is agnostic as to whether it is served by a threaded, blocking server or an asynchronous, non-blocking one.  The simplest way to serve a non-blocking :ref:`weblayer` application is to deploy it behind `Gunicorn`_.

To use :ref:`weblayer` with `Gunicorn`_:

* follow the instructions above on deploying with :ref:`Paste`
* amend your `[server:main]` section, as per `these instructions  <http://gunicorn.org/configure.html#paster-applications>`_, e.g.:

::

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

When these issues are resolved, it may be appropriate for :ref:`weblayer` to provide some sort of native web socket aware request handler.  Until then, simply use existing `WSGI`_ middleware, such as `gevent-websocket`_ and then look in `environ['wsgi.websocket']` or `environ['wsgi.input']` (or wherever the middleware sticks the reference to the socket) when writing request handler code, e.g.::

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
            
        
    


.. _`./src/weblayer/examples/deploy/paste`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/deploy/paste
.. _`./src/weblayer/examples/deploy/appengine`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/deploy/appengine
.. _`./src/weblayer/examples/deploy/mod_wsgi`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/deploy/mod_wsgi
.. _`amending sys.path`: http://www.johnny-lin.com/cdat_tips/tips_pylang/path.html
.. _`apache mod_wsgi`: http://code.google.com/p/modwsgi
.. _`egg`: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _`gevent`: http://www.gevent.org/
.. _`gevent-websocket`: http://pypi.python.org/pypi/gevent-websocket/
.. _`google app engine`: http://code.google.com/appengine/
.. _`gunicorn`: http://gunicorn.org/
.. _`gunicorn documentation`: http://gunicorn.org/
.. _`paste.app_factory`: http://pythonpaste.org/deploy/
.. _`paste config values`: http://pythonpaste.org/deploy/#config-format
.. _`paster serve`: http://pythonpaste.org/script/#paster-serve
.. _`python`: http://www.python.org
.. _`python path`: http://code.google.com/appengine/docs/python/runtime.html
.. _`setup.py`: http://github.com/thruflo/weblayer/tree/master/setup.py
.. _`your apache configuration`: http://code.google.com/p/modwsgi/wiki/QuickConfigurationGuide
.. _`websocket`: http://en.wikipedia.org/wiki/WebSockets
.. _`wsgi`: http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
.. _`wsgiscriptalias directive`: http://code.google.com/p/modwsgi/wiki/ConfigurationDirectives
