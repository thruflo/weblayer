
`weblayer`_ is a `Python`_ package for web developers who like making their own design decisions.  Built on `WebOb`_, it provides a set of components that can be used to handle requests and create a `WSGI`_ application.

It is not a framework.  In contrast, `weblayer`_ tries to prescribe as little as possible, allowing you to swap out components and work with your weapons of choice.  It's fast and fully tested.  The `source code`_ is documented and includes `examples`_.


Install
-------

`weblayer`_ requires `Python`_ version 2.5 to 2.7.  Install it via the `Python Package Index`_, e.g.::

    easy_install weblayer

Or::

    pip install weblayer


Develop
-------

To develop (or play around with) it, get the `source code`_, either using `Git`_::

    git clone ... # @@

Or from the Python Package Index, e.g.::

    wget # @@ 
    tar -zxvf weblayer-0.3.tar.gz
    
Develop the egg::

    cd weblayer
    python setup.py develop

Install the additional dependencies::

    easy_install weblayer[dev]

Run the tests::

    ./bin/nosetests -c etc/nose.cfg
    
Generate the docs::

    ./bin/sphinx-build -a -b html docs docs/_build

If you have any problems or suggestions, `Github Issues`_ is the place to raise a ticket.


.. _`weblayer`: #
.. _`source code`: #
.. _`examples`: #
.. _`a simple hello world`: #
.. _`Apache using mod_wsgi`: #
.. _`Nginx using Gunicorn`: #
.. _`Google App Engine`: #
.. _`Github Issues`:

.. _`Git`: # 
.. _`Python`: #
.. _`Python Package Index`: #
.. _`repoze.bfg`: #
.. _`Tornado`: #
.. _`webapp`: #
.. _`weblite`: #
.. _`WebOb`: #
.. _`weukzeug`: #
.. _`WSGI`: #
.. _`zope.component`: #

