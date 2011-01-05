
Getting Started
===============


Install
-------

:ref:`weblayer` requires `Python`_ version 2.5 to 2.7.  Install it via the `Python Package Index`_, e.g.::

    easy_install weblayer

Or::

    pip install weblayer

See the :ref:`Hello World` for example usage.


Develop
-------

To develop (or play around with) it, get the `source code`_, either using `Git`_::

    git clone git://github.com/thruflo/weblayer.git

Or from a release tarball, e.g.::

    wget http://pypi.python.org/packages/source/w/weblayer/weblayer-0.3.tar.gz
    tar -zxvf weblayer-0.3.tar.gz
    
Develop the egg::

    cd weblayer
    python setup.py develop

Install the additional dependencies::

    easy_install weblayer[dev]

Run the tests::

    ./bin/nosetests -c etc/nose.cfg
    
Generate the docs::

    ./bin/sphinx-build -a -b html doc doc/_build

If you have any problems or suggestions, `Github Issues`_ is the place to raise a ticket.

.. _`git`: # 
.. _`github issues`: #
.. _`helloworld.py`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/helloworld.py
.. _`python`: #
.. _`python package index`: #
.. _`source code`: #
.. _`weblayer`: #
