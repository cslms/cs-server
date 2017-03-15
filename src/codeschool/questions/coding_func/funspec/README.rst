Funspec
=======

Funspec is an specification for grading programming questions based on
functions. It is built on top of Iosepc + an specific layout of a python module.
In funspec, we define the functions that will be used as the answer key using
the @answer_key decorator::

    @answer_key
    def double(x: int):
        return x + x

One can specify generic input values using type hints. In the above example,
the funspec tester will create a series of integer examples for ``x`` and
compare the results from the ``double`` function defined by the student with
the answer key.

A simple type specification can be too broad: the test function should handle
just a subset of the integers, or maybe only strings of some specific type. In
many cases, these extra restrictions can be easily represented by Iospec
commands, which funspec gladly accepts::

    @answer_key
    def double(x: '$int(0, 1000)'):
        return x + x

Now the function will be tested only with integers in the 0-1000 interval.
