
Getting Started
===============

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

Or from a release tarball, e.g.::

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


.. _`git`: # 
.. _`github issues`: #
.. _`python`: #
.. _`python package index`: #
.. _`source code`: #
.. _`weblayer`: #
