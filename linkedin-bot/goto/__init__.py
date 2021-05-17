"""GOTO: A function decorator, that rewrites the bytecode, to enable goto in Python.


    AUTHOR
==============

Name: Sebastian Noack
GitHub: https://github.com/snoack
Location: Detroit, MI, United States
Gmail: sebastian.noack@gmail.com


    REPOSITORY
==================

Python Goto GitHub Repository: https://github.com/snoack/python-goto

A function decorator to use `goto` in Python. Tested on Python 2.6 through 3.7 and PyPy.


    INSTALLATION
====================

$ pip install goto-statement


    USAGE
=============

from goto import with_goto

@with_goto
def range(start, stop):
    i = start
    result = []
    
    label .begin
    
    if i == stop:
        goto .end
    
    result.append(i)
    i += 1
    
    goto .begin
    label .end
    
    return result


    IMPLEMENTATION
======================

Note that `label .begin` and `goto .begin` is regular Python syntax to retrieve the attribute `begin` 
from the objects with the variable names `label` and `goto`. However, in the example above these variables 
aren't defined. So this code would usually cause a `NameError`. But since it's valid syntax the function 
can be parsed, and results in following bytecode:


  5           0 LOAD_FAST                0 (start)
              2 STORE_FAST               2 (i)
  6           4 BUILD_LIST               0
              6 STORE_FAST               3 (result)
  8           8 LOAD_GLOBAL              0 (label)
             10 LOAD_ATTR                1 (begin)
             12 POP_TOP
  9          14 LOAD_FAST                2 (i)
             16 LOAD_FAST                1 (stop)
             18 COMPARE_OP               2 (==)
             20 POP_JUMP_IF_FALSE       28
 10          22 LOAD_GLOBAL              2 (goto)
             24 LOAD_ATTR                3 (end)
             26 POP_TOP
 12     >>   28 LOAD_FAST                3 (result)
             30 LOAD_METHOD              4 (append)
             32 LOAD_FAST                2 (i)
             34 CALL_METHOD              1
             36 POP_TOP
 13          38 LOAD_FAST                2 (i)
             40 LOAD_CONST               1 (1)
             42 INPLACE_ADD
             44 STORE_FAST               2 (i)
 14          46 LOAD_GLOBAL              2 (goto)
             48 LOAD_ATTR                1 (begin)
             50 POP_TOP
 16          52 LOAD_GLOBAL              0 (label)
             54 LOAD_ATTR                3 (end)
             56 POP_TOP
 17          58 LOAD_FAST                3 (result)
             60 RETURN_VALUE


The `with_goto` decorator then removes the respective bytecode that has been generated for the attribute 
lookups of the `label` and `goto` variables, and injects a `JUMP_ABSOLUTE` or `JUMP_RELATIVE` instruction 
for each `goto`:


  5           0 LOAD_FAST                0 (start)
              2 STORE_FAST               2 (i)
  6           4 BUILD_LIST               0
              6 STORE_FAST               3 (result)
  8           8 NOP
             10 NOP
             12 NOP
  9     >>   14 LOAD_FAST                2 (i)
             16 LOAD_FAST                1 (stop)
             18 COMPARE_OP               2 (==)
             20 POP_JUMP_IF_FALSE       28
 10          22 JUMP_FORWARD            34 (to 58)
             24 NOP
             26 NOP
 12     >>   28 LOAD_FAST                3 (result)
             30 LOAD_METHOD              4 (append)
             32 LOAD_FAST                2 (i)
             34 CALL_METHOD              1
             36 POP_TOP
 13          38 LOAD_FAST                2 (i)
             40 LOAD_CONST               1 (1)
             42 INPLACE_ADD
             44 STORE_FAST               2 (i)
 14          46 JUMP_ABSOLUTE           14
             48 NOP
             50 NOP
 16          52 NOP
             54 NOP
             56 NOP
 17     >>   58 LOAD_FAST                3 (result)
             60 RETURN_VALUE



    ALTERNATIVE IMPLEMENTATION
==================================

The idea of `goto` in Python isn't new.

There is [another module](http://entrian.com/goto/) that has been released as April Fool's joke in 2004. 
That implementation doesn't touch the bytecode, but uses a trace function, similar to how debuggers are written.
While this eliminates the need for a decorator, it comes with significant runtime overhead and a more elaborate 
implementation. Modifying the bytecode, on the other hand, is fairly simple and doesn't add overhead at function
execution.
"""

__name__ = "Goto"
__package__ = "Goto"
__version__ = "1.2.0"
