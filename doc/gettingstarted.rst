
Getting Started
===============


Install
-------

:ref:`weblayer` requires `Python`_ version 2.5 to 2.7.  Install it via the
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

.. _`git`: http://git-scm.com/
.. _`github issues`: http://github.com/thruflo/weblayer/issues
.. _`python`: http://www.python.org
.. _`python package index`: http://pypi.python.org/pypi/weblayer
.. _`source code`: http://github.com/thruflo/weblayer
