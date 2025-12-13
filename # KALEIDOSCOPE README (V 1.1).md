# KALEIDOSCOPE README (V 1.1)
## INTRODUCTION

This documentation is for the Kaleidoscope Framework, a template bundled with modules that allows you to make your own programming language using different engines. I recommend gaining some experience with Python prior to using the framework.

In the Kaleidoscope.zip folder, there is a __init__ and three folders labeled Examples, Modules, and Direct Code. The __init__ is not to be messed with, except if you know what you are doing (or if you want to read it).

The Examples folder simply contains an example (+ any future ones) of a language made with Kaleidoscope or as a proof-of-concept. 

The Modules folder is not meant to be interacted with directly; instead, its contents are to be imported from their folder and used as if they were modules.

The Direct Code folder contains templates in the framework meant to be interacted with directly and edited to achieve your goal.

## HOW TO GET STARTED

To get started, simply import a module from the Modules folder or open up one of the Direct Code files! I recommend reading further in the README as well, because it'll help tremendously when creating your own language or assembling a premade language!

## MODULES

### tokenfunctions.py

tokenfunctions is a general-purpose module for interpreting and defining syntax. It contains three functions: error, define, and interpreter.

The error function takes strings as its arguments. It is the message that displays when invalid syntax occurs.

The define function takes strings (no whitespace) as its arguments. This is what defines your syntax into a prebuilt dict (syntax). Its arguments include the character(s), and the Python code that executes upon encountering that character. (Ex: tokenfunctions.define(">", """print("hi")"""))

The interpreter function takes a string as its argument (this would be the finished program you wish to run) and processes it (lexing, parsing, interpreting), and executes according to your syntax dict definitions.

The code looks like this:
```syntax = {

}

def error(string):
    global errormessage
    errormessage = string

def define(char, code):
    syntax[char] = code

def interpreter(program):
    global finalizedprogram
    finalizedprogram = program.split(# Empty here --- This will split on any whitespace)
    for token in finalizedprogram:
        if token not in syntax:
            print(errormessage)
        else:
            exec(str(syntax[token]))``

### syntaxfunc.py

syntaxfunc.py is a module that includes a set of pre-built syntax + an execution function (called syntaxprocessor). The prebuilt syntax is mapped to individual Python tokens to allow for dynamic if/then statements. In order to make other dynamic conditional, such as loops, you will need to map to Python or execute other code.

The code looks like this:
``draft = []

syntax = {
    "if": "if",
    "then": ":\n    ",
    "end": "\n",
    "true": "True"
}

def syntaxprocessor(program):
    for item in program:
        if item in syntax:
            item = syntax[item]
            draft.append(item)
        else:
            draft.append(item)```

The `draft` list is there to preserve code and run it later, and the syntaxprocessor() function is there for remapping and processing.

## DIRECT CODE

The Direct Code folder contains three .py's, meant to be edited directly and provide more abstraction than the modules would. Currently, there is the single-char engine, the REPL engine, and the instruction set engine.

### SINGLE-CHAR ENGINE

The single-char engine is meant to function with single character syntax (like Brainfuck). Its code is also stored in a dict but you can also edit prerequisite code (code executed before the dict code) in the match statement, **i** section.

The **i** section should look like this:
```        while i < len(userinput):
            ch = userinput[i]
            match ch:
                case "x":
                    code = syntax[ch]
                    exec(code)
                    i += 1
                case "x":
                    code = syntax[ch]
                    exec(code)
                    i += 1
                case "x":
                    code = syntax[ch]
                    exec(code)
                    i += 1
                case "x":
                    code = syntax[ch]
                    exec(code)
                    i += 1
                case "x":
                    code = syntax[ch]
                    exec(code)
                    i += 1```

This is what executes the code from the syntax dict. You can change the code in the syntax dict to match up with your single-char token, and also add code that executes before your syntax dict code does, mainly for debugging.

Example:
```               case "$":
                    print("This is prerequesite code")
                    code = syntax[ch] # This sets the execution code
                    exec(code)
                    i += 1```

An **n** section is also included in the match statement, mainly for setting addresses or indexes for more complex operations such as loops.

It looks as such:
```        while n < len(userinput):
            ch = userinput[n]
            match ch:
                case "x":
                    n += 1
                case "x":
                    n += 1
                case "x":
                    n += 1
                case "x":
                    n += 1
                case "x":
                    n += 1
                case "x":
                    n += 1
                case "x":
                    n += 1```

This, if you aren't making anything complex, can be untouched entirely. But if your goal is to make something more complex than Brainfuck without loops, then it may be required to use.

Example:
```                case "x":
                    index.append(n) # This is simply a placeholder for whatever indexing routine you use
                    n += 1```

### INSTRUCTION SET ENGINE

The instruction set engine is built to handle custom high-level and low-level instructions, as assembly uses, but syntax + semantics must be constructed themselves, and routines/functions and loops be crafted by the author themselves.

The lexer/parser/interpreter looks like this:
```def interpreter(program):
    i = 0
    try:
        if i == log.index(-1):
            i = j
            program = backup
    except Exception:
        pass
    while i < len(program):
        for instr in program:
            try:
                match instr.split(): # Lexer
                    case ["plc", reg, reg2] if reg in registers and reg2 in registers: # [Lists = Parser]
                        pass
            except Exception:
                print("error")```

This function contains the entire Lexer Parser Interpreter loop. You replace the "plc" instruction with whatever instructions you add, and its semantics below the case statement.
Example:
```            try:
                match instr.split():
                    case ["add", reg, reg2] if reg in registers and reg2 in registers: # Instruction
                        reg += reg2 # Semantics
            except Exception:
                print("error")```

The file also contains a JSON input system, which allows your programs to work.
It should look like this:
```try:
    with open(filename, "r") as macro:
        program = json.load(macro)
        for line in program:
            print(line)
except FileNotFoundError:
    pass

try:
    while True:
        userinput = input()
        if userinput == "/exit":
            raise SystemExit
        elif userinput == "/run":
            with open(filename, "w") as macro:
                json.dump(program, macro)

            with open(filename, "r") as macro:
                json.load(macro)
                interpreter(program)
        else:
            text = userinput
            program.append(text)

except SystemExit:
    with open(filename, "w") as macro:
        json.dump(program, macro)```

This, as you can see, also contains /slash commands reminiscent of Discord or Minecraft. These /slash commands are used to control the file outside of the program (for things of user's convenience, such as /erase, which erases a program).
Example:
```try:
    while True:
        userinput = input()
        if userinput == "/exit":
            raise SystemExit```

Finally, there is a set of variables at the top of the program. These should be edited to your own functionality/convenience.
It looks like this:
```import json

filename = "placeholder"
program = []
memory = {}
stack = [0] * 65535
routines = {}
loops = {}
registers = {}
i = 0
j = 0
log = []
backup = []```

### REPL ENGINE

There is a simple REPL/Interactive Shell engine contained in the Direct Code folder.
The code looks like this:
```variables = {}
error = "error"

while True:  # Loop
    userinput = input().split()
    match userinput:
        case ["set", var, value]:  # Read
            try:  # Eval
                variables[var] = int(value)
            except Exception:
                print(error)```

Simply put, this takes a single line of code and parses it instantly. Setting works like the instruction set file.
Example:
``        case ["set", var, value]:  # Read
            try:  # Eval
                variables[var] = int(value)
            except Exception:

                print(error)``
