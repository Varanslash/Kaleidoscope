import json

# Memory

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

# General Processor

def interpreter(program):
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
                match instr: # Lexer
                    case ["plc", reg, reg2] if reg in registers and reg2 in registers: # [Lists = Parser]
                        pass

# Text Editor

try:
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
        json.dump(program, macro)