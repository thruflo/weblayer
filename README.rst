
``thruflo.webapp`` is a WSGI compatible web application framework.  It has no test coverage and is no doubt flawed.  But it has the advantage of being setup just the way I want it:

* ``re.compile`` based url mapping
* class instances handling requests with methods that correspond to the HTTP Request's method, e.g.: ``def post(self)`` handles a `POST` request
* a ``webob.Request`` as self.request
* ``return foo`` as the method of responding, where ``foo`` can be a string, a ``webob.Response``, or a ``list`` or ``dict`` to be returned as JSON
* `mako templates`_ with builtin methods including:
  * ``static_url``
  * ``xsrf_form_html``
  * ``escape``, as well as references to
  * ``handler`` and 
  * ``request``

Or to put it another way::

    from thruflo.webapp import web
    
    class Hello(web.RequestHandler):
        def get(self):
            return 'hello world'
            
        
    
    mapping = [('/.*', Hello)]
    application = web.WSGIApplication(mapping)
    

See `thruflo.webapp.demo`_ for a slightly fleshed out example usage.

.. _`mako templates`: http://www.makotemplates.org
.. _`thruflo.webapp.demo`: http://github.com/thruflo/thruflo.webapp/tree/master/src/thruflo/webapp/demo/
