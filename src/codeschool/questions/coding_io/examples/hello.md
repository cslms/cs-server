Hello Person
============

    Author: chips
    Type: io
    
Your second program.


Description
-----------

Create a program that asks a name and prints the message "Hello <name>!" on 
screen.

### Example

    name: <john>
    Hello john!

Tests
-----

    name: <john>
    Hello john!
    
    name: <john lennon>
    Hello john lennon!
    
    
Hidden Tests
------------

    @input $name
    
    
Answer key (python)
-------------------

    name = input('name: ')
    print('Hello %s!' % name)
 