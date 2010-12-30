`weblayer`_ is a `Python`_ package for web developers who like making their own design decisions.  Built on `WebOb`_, it provides a set of components that can be used to handle requests and create a `WSGI`_ application.

It is not a framework.  In contrast, `weblayer`_ aims for low cognitive overhead and to prescribe as little as possible, allowing you to swap out components and work with your weapons of choice.  Similar in utility to `weukzeug`_, it builds on aspects of `repoze.bfg`_, `Tornado`_, Google's `webapp`_ and Tav's `weblite`_ (and uses `zope.component`_ under the hood).

It's fast and fully tested.  The source code is documented and contains examples showing how to use it, including `a simple hello world`_ and deployments behind `Apache using mod_wsgi`_, `Nginx using Gunicorn`_ and on `Google App Engine`_.

To use it, simply install the egg, e.g.::

    easy_install weblayer

To develop or play around with it, get `the source code`_ using `Git`_::

    git clone ... # @@

Develop the egg::

    cd weblayer
    python setup.py develop

Install the additional dependencies::

    easy_install weblayer[dev]

Run the tests::

    ./bin/nosetests -c etc/nose.cfg
    
Generate the docs::

    ./bin/sphinx-build -a -b html docs docs/_build

If you have any problems or suggestions `Github Issues`_ is the place to raise a ticket.

.. _`weblayer`: #
.. _`the source code`: #
.. _`a simple hello world`: #
.. _`Apache using mod_wsgi`: #
.. _`Nginx using Gunicorn`: #
.. _`Google App Engine`: #
.. _`Github Issues`:

.. _`Git`: # 
.. _`Python`: #
.. _`repoze.bfg`: #
.. _`Tornado`: #
.. _`webapp`: #
.. _`weblite`: #
.. _`WebOb`: #
.. _`weukzeug`: #
.. _`WSGI`: #
.. _`zope.component`: #

