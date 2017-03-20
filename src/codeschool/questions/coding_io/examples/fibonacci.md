Fibonacci
=========

    Author: chips
    Type: io
    
A famous sequence.


Description
-----------

The Fibonacci sequence starts with 1, 1 and each new number is created by adding
the two previous numbers. Create a program that asks a number N of terms of
the Fibonacci sequence that should be printed on screen.

### Example

    n: <8>
    1
    1
    2
    3
    5
    8
    13
    21

Tests
-----

    n: <8>
    1
    1
    2
    3
    5
    8
    13
    21
    
    @input $int(2, 100)
    
    
Hidden Tests
------------

    @input 1
    @input 100
    
    
Answer key (python)
-------------------

    n = int(input('n: '))
    x, y = 1, 1
    for _ in range(n):
        print(x)
        x, y = y, x + y
