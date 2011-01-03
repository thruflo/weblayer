
=======
Recipes
=======


Use Cases
=========

Async / Non-blocking
--------------------

`weblayer`_ is agnostic as to whether it is served by a threaded, blocking server or an asynchronous, non-blocking one.  The simplest way to serve an `IO bound`_ application with a non-blocking server is to `deploy it behind Gunicorn`_ using the `gevent worker class`_.

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
            
        
    

@@ double check websockets make GET requests...


Deployment
==========

Apache mod_wsgi
---------------

@@ ...

Paste
-----


Gunicorn
--------

`Gunicorn`_ is a `Python`_ server that allows a web application to be served using either synchronous or asynchronous worker classes.  See `Gunicorn's documentation` for more information, especially the section on `how to deploy Gunicorn behind Nginx`_.

Once you have `Gunicorn`_ installed and configured, it's trivial to serve a non-blocking `weblayer`_ application.  @... paste ...


Appengine
---------

As a pure `Python`_ package, `weblayer`_ works perfectly on `Google App Engine`_.  Imagine you have the following minimal `app.yaml`_ (replacing `<<yourappid>>` with your application id):

.. literalinclude:: ../src/weblayer/examples/appengine/app.yaml

You then need to return a WSGI application from a static `main` function in `app.py`, e.g.:

.. literalinclude:: ../src/weblayer/examples/appengine/app.py
   :linenos: 
   :lines: 10-
