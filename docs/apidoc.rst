=============
API Reference
=============

All Codeschool modules and apps live inside the codeschool namespace. Besides
these core modules, the Codeschool team also maintains a few modules as external
dependencies. This page gives an overview of the architecture and the role
each module plays in the Codeschool infrastructure.


Core services
=============


Core modules
============

- fixes: monkey-patch 3rd party libs
- components: jinja2/bricks components
- settings: django settings
- site: core templates


Core apps
=========

- accounts: user authentication, login and signup (uses userena)
- cli: command line scripts that helps managing codeschool
- core: a mixed bag of core functionality


Learning management system
==========================

- lms: learning management system, control courses, grades, etc


Questions
=========

- questions: implement different question types


Extra
=====

- extra: optional codeschool activities
- gamification: points, badges and stars
- social: social network capabilities


Testing framework
=================

Codeschool uses `pytest`_ as a testing framework. The :mod:`codeschool.tests` module
provides an infrastructure with some useful fixtures, mocks, factories
and abstract test case classes.

.. _pytest: https://pytest.org


Each app must provide a /tests/ module which is typically divided in the
following structure.

**tests/test_appname.py**
Unit tests that tests the main module functionality
and makes little or no access to the database. These tests should run fast and
are used in a TDD development cycle.

**test/test_db.py**
unittests that make database access. These module should
be marked with the `pytest.mark.test_db` mark and are excluded from the default
test suite. They should be executing before pushing any commit.

**test/test_views.py**
Test view functions and check if the urls exposed by the app are functional.
These tests typically uses both the database and Django's request factory
objects. This module should be marked with `pytest.mark.test_views` mark.

**test/test_ui.py**
These module should hold all tests that uses the web driver. This is the slowest
part of the test suite and should be marked with `pytest.mark.test_ui`


Transition
----------
Most Codeschool test folders are currently organized into two modules: `test_unit.py`
and `test_integrations.py`. This is a temporary arrengment until we refactor old
tests into the new infrastructure.


See also
--------

.. toctree::
   :maxdepth: 2

   Testing <testing.rst>


External modules
================

- vendor: vendorized libs
