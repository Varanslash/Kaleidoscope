# KALEIDOSCOPE README (V 1.0)
## INTRODUCTION

This documentation is for the Kaleidoscope Framework, a template bundled with modules that allows you to make your own programming language using different engines. 

In the Kaleidoscope.zip folder, there is a __init__ and three folders labeled Examples, Modules, and Direct Code. The __init__ is not to be messed with, except if you know what you are doing (or if you want to read it).

The Examples folder simply contains an example (+ any future ones) of a language made with Kaleidoscope or as a proof-of-concept. 

The Modules folder is not meant to be interacted with directly; instead, it is to be imported from its folder and used as if it was a module.

The Direct Code folder contains templates in the framework meant to be interacted with directly and edited to achieve your goal.

## MODULES

In the modules folder there is a single .py file (more to come!). It contains three functions: error, define, and interpreter.

The error function takes strings as its arguments. It is the message that displays when invalid syntax occurs.

The define function takes strings (no whitespace) as its arguments. This is what defines your syntax into a prebuilt dict (syntax). Its arguments include the character(s), and the Python code that executes upon encountering that character. (Ex: tokenfunctions.define(">", """print("hi")"""))

The interpreter function takes a string as its argument (this would be the finished program you wish to run) and processes it (lexing, parsing, interpreting), and executes according to your syntax dict definitions.

## DIRECT CODE

The Direct Code folder contains two .py's, meant to be edited directly and provide more abstraction than the modules would. Currently, there is the single-char engine, and the instruction set engine.

The single-char engine is meant to function with single character syntax (like Brainfuck). Its code is also stored in a dict but you can also edit prerequisite code (code executed before the dict code) in the match statement, **i** section.

The instruction set engine is built to handle custom high-level and low-level instructions, as assembly uses, but syntax + semantics must be constructed themselves, and routines/functions and loops be crafted by the author themselves.
