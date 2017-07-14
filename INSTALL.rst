=========================
Installation instructions
=========================

First step is to clone the git repository::

    $ git clone https://github.com/cslms/cs-server.git
    $ cd cs-server

At this point you might want to create a virtualenv, in order to isolate
Codeschool and its many dependencies from your Python environment. First check
if virtualenvwrapper is available in your distribution (e.g., ``sudo apt-get install virtualenvwrapper``)
If it is not available, install it from pip (``pip install virtualenvwrapper``),
then execute::

    $ virtualenvwrapper.sh
    $ mkvirtualenv codeschool -p /usr/bin/python3
    $ workon codeschool

Move to the source tree and install all pip dependencies. This may take a while.

::

    $ python setup.py develop
    $ pip install -e .[dev]


Javascript deps
---------------

If you want to make any frontend development, the next step should be installing
the correct Javascript packages from npm. Codeschool uses Elm + Polymer as the
main frontend language/framework. It also uses `Webpack`_ to create "bundles" of
web resources and to generate the final production build. Stylesheets are handled
using the Sass pre-processor.

Each of those technologies require a different

You need node.js and npm to make it work::

    Debian
    $ apt-get install nodejs npm

    Arch linux
    # pacman -S npm

.. _Webpack: https://webpack.github.io/

After you have npm installed, execute::

    $ npm install

Redis
-----

Codeschool uses redis for cache. Redis must be installed and running before you
start codeschool.

::

    Debian
    $ apt-get install redis-server

    Arch linux
    $ redis-server


Invoke tasks
------------

Codeschool uses `invoke`_ to control several aspects of development and
deployment. We start with the invoke task::

    $ inv develop

This will download the Javascript dependencies, build the necessary bundles
with webpack, and then initialize the sqlite3 database. Codeschool is
database-agnostic, and you probably want to use a real database server such as
Posgres or MySQL in production.

Test it!
--------

Finally, run the development sever and point your browser to http://localhost:8000::

    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py runserver

.. _invoke: http://www.pyinvoke.org
