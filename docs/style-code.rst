============
Coding style
============

We use PEP8 as the base coding style. This basic style is enforced by `flake8`_
and `autopep8`_ tools. In order to check PEP8 compliance, just run::

    $ flake8

from the codeschool root folder. `autopep8` requires the recursive and inplace
options::

    $ autopep8 src/codeschool -ir

.. _flake8: http://flake8.pycqa.org/en/latest/
.. _autopep8: https://github.com/hhatto/autopep8


Differences from PEP8
---------------------

**Line lengths**

Line length is encouraged to be under 79 characters but this is not enforced.
It is acceptable to have slightly longer lines if it avoids to break lines in
a few sittuations. We leave to the humans to decide.


**Named lambdas**

PEP8 encourages using def's instead of named lambdas. We don't see a problem
with named lambdas and Python def's can be really cumbersome when using
a more functional style. While Codeschool uses an object oriented archtecture,
we value immutability and functional styles.


Other considerations
--------------------

We favor single quoted strings and triple-single-quoted strings for most cases.
Double quoted strings are reserved mostly to docstrings. You can use double
quotes if the string content has single quotes::

    # Do
    st1 = 'foo'
    st2 = '''multi
    line
    string'''
    st3 = "good'ol string"

    # Don't
    st4 = "foo"
    st5 = """multi
    line"""


Naming conventions
------------------

Use always `CamelCase` for class names and `snake_case` for everything else.
Functions and methods usually should be named after verbs if they introduce
side-effects and should be substantives if they are pure-ish functions that simply
return some value from the given arguments.

Try to avoid functions that both produce a side-effect and return an useful
value. This is usually a symptom of a poor architecture and should be refactored
into separate functions that perform each step separately.

Python cannot enforce strictly separation of functional/pure vs. impure code.
Mild side-effects are acceptable. Do not worry too much about those cases:

* Logging: this is a side-effect that we can simply ignore.
* Cache: although caching is technically a side-effect, it is just a simple
  optimization. Usually it is good to expose a non-cached version of the
  function for testing.
* Singletons: computation is performed and stored in a global state. This
  obviously has side-effects, but we can treat as a form of caching. You
  probably need to take some measures to make singletons testable and provide
  some function to reset the global state across unittests. In any case,
  avoid using singletons when possible.


Docstrings
----------

Docstrings use Google style (`google-style`_):

.. code-block:: python

    class MyClass:
        """
        A short (usually 1-sentence) description.

        An optional longer description that detail the class usage and
        additional assumptions and principles used to implement it.

        Attrs:
            attr_name (type):
                Description.

        Examples:
            Put some doctests with examples of how to use your class.
            >>> x = MyClass()
            >>> x.say_hello()
            "Hello!"
        """

        def some_method(self, arg1, arg2):
            """
            Short description.

            Optional long description.

            Examples:
                >>> x.some_method(1, 2)
                3

            Args:
                arg1 (type):
                    Argument description
                arg2 (type):
                    arg2 description

            Raises:
                Does it raise any exception? When?

            Returns:
                Description of the return value.


            See also:
                Additional information and links to other methods or functions.
            """

Observations:

**Docstrings should always triple-double-quoted and start with an empty line.**

Do::

    def sqrt(x):
        """
        Return the square root of x.
        """
        ...

Don'ts::

    def sqrt(x):
        """Return the square root of x."""
        ...

    def sqrt(x):
        '''
        Return the square root of x.
        '''
        ...


**Very short docstrings can use single double-quotes.**

::

    def sqrt(x):
        "Return the square root of x."

This is specially desirable when defining a sequence of very small functions.


.. _google-style: http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


Type hints
----------

Python 3 introduced type hints, but they were largely ignored by the community.
Type hints have no defined runtime semantics and they are mostly used to
help static analyzers and IDEs to reason about Python code.

Type hints are a **good idea**, but we are admittedly a little bit lazy to put
them in most of our codebase. We encourage new code to use them and accept
patches that introduce type hints in existing code. The typing module introduced
in Python 3.5 is always allowed.

If you never saw a type hint in Python, here is an example::

    def fib(n: int) -> int:
        """
        Returns the n-th Fibonacci number using an awful algorithm :)
        """
        return fib(n - 1) + fib(n - 2) if n > 1 else 1


Architectural guidelines
------------------------

* Prefer immutable data structures over mutable ones.
* Prefer pure functions over classes.
* Prefer classes over impure functions.
* Avoid fat views: a view should collect information from the database and
  only perform simple business logic (e.g., check permissions)
* Avoid fat models: the main concern of a model is validation and keeping
  consistency of its own data.
* Table-level manipulation should be done in managers/querysets.


Inconsistencies
---------------

Sometimes we violate our own rules (Oooops!). Codeschool has some legacy code
written prior this coding style. We value consistency, but we also live in the
real world and acknowlegdge things are not always perfect. If you spot something
fishy, please submit an issue (or better yet, a pull request).
