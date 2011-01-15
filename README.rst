`weblayer`_ is a `Python`_ package, built on `WebOb`_, that provides a set of
components that can be used to handle requests within a `WSGI`_ application.

It is not a framework.  In contrast, `weblayer`_ tries to prescribe as little
as possible, allowing you to swap out components and work with your weapons 
of choice.

It's fast, tested and `documented`_.  The `source code`_ is `public domain`_.

Install
-------

`weblayer`_ requires `Python`_ version 2.5 to 2.7.  Install it via the
`Python Package Index`_, e.g.::

    easy_install weblayer

Or::

    pip install weblayer

Develop
-------

To develop (or play around with) it, get the `source code`_, either using
`Git`_::

    git clone git://github.com/thruflo/weblayer.git
    cd weblayer

Or from a release tarball, e.g.::

    wget http://github.com/thruflo/weblayer/tarball/master
    tar -zxvf thruflo-weblayer-*.tar.gz
    cd thruflo-weblayer-*

Develop the egg::

    python setup.py develop

Install the additional dependencies::

    easy_install weblayer[dev]

Run the tests::

    ./bin/nosetests -c etc/nose.cfg
    
Generate the docs::

    ./bin/sphinx-build -a -b html doc doc/_build

If you have any problems or suggestions, `Github Issues`_ is the place to raise a ticket.

Usage
-----

See the `User Guide`_ and `examples`_ for more information.

.. _`documented`: http://packages.python.org/weblayer
.. _`examples`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples
.. _`git`: http://git-scm.com/
.. _`github issues`: http://github.com/thruflo/weblayer/issues
.. _`public domain`: http://creativecommons.org/publicdomain/zero/1.0/
.. _`python`: http://www.python.org
.. _`python package index`: http://pypi.python.org/pypi/weblayer
.. _`source code`: http://github.com/thruflo/weblayer
.. _`user guide`: http://packages.python.org/weblayer/userguide.html
.. _`weblayer`: http://packages.python.org/weblayer
.. _`webob`: http://pythonpaste.org/webob/
.. _`wsgi`: http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
