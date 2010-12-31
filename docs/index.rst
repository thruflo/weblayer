
======================
weblayer Documentation
======================


Getting Started
===============

.. include:: ../README.rst

Hello World
-----------

You can then write code like this:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
  :language: python


User Guide
==========

.. include:: ../USERGUIDE.rst

Deployment
----------

@@ deployment ...

* paste
* gunicorn
* mod_wsgi
* appengine


Modules
=======

weblayer.auth
-------------

.. automodule:: weblayer.auth
   :members:

weblayer.base
-------------

.. automodule:: weblayer.base
   :members:

weblayer.bootstrap
------------------

.. automodule:: weblayer.bootstrap
   :members:

weblayer.component
------------------

.. automodule:: weblayer.component
   :members:

weblayer.cookie
---------------

.. automodule:: weblayer.cookie
   :members:

weblayer.interfaces
-------------------

.. automodule:: weblayer.interfaces
.. autointerface:: weblayer.interfaces.IAuthenticationManager
.. autointerface:: weblayer.interfaces.IMethodSelector
.. autointerface:: weblayer.interfaces.IPathRouter
.. autointerface:: weblayer.interfaces.IRequest
.. autointerface:: weblayer.interfaces.IRequestHandler
.. autointerface:: weblayer.interfaces.IResponse
.. autointerface:: weblayer.interfaces.IResponseNormaliser
.. autointerface:: weblayer.interfaces.ISecureCookieWrapper
.. autointerface:: weblayer.interfaces.ISettings
.. autointerface:: weblayer.interfaces.IStaticURLGenerator
.. autointerface:: weblayer.interfaces.ITemplateRenderer
.. autointerface:: weblayer.interfaces.IWSGIApplication

weblayer.method
---------------

.. automodule:: weblayer.method
   :members:

weblayer.normalise
------------------

.. automodule:: weblayer.normalise
   :members:

weblayer.request
----------------

.. automodule:: weblayer.request
   :members:

weblayer.route
--------------

.. automodule:: weblayer.route
   :members:

weblayer.settings
-----------------

.. automodule:: weblayer.settings
   :members:

weblayer.static
---------------

.. automodule:: weblayer.static
   :members:

weblayer.template
-----------------

.. automodule:: weblayer.template
   :members:

weblayer.utils
--------------

.. automodule:: weblayer.utils
   :members:

weblayer.wsgi
-------------

.. automodule:: weblayer.wsgi
   :members:
