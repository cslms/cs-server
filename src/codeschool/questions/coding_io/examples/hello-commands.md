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

    @command
    def answer(*args):
        return 42
    
    x: $name
    ...
    
    @input $int(1, 100)
    @input $answer
    
    x: <foo>
    foo

    
    
Hidden Tests
------------

    @input $name
    
    
Answer key (python)
-------------------

    name = input('name: ')
    print('Hello %s!' % name)
 