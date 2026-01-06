 # Imports (for controlling the processor)

import sys
import time
import json

# Memory

filename = "extprocessor"
program = []
backendmemory = list(range(65536))
memory = [hex(num) for num in backendmemory]
stack = [0] * 65535
routines = {}
loops = {}
registers = {
    "x": 0,
    "y": 0,
    "z": 0,
    "a": 0,
    "b": 0,
    "c": 0,
    "r": 0,
    "e": 0
}
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
                    case ["xor", reg, reg2] if reg in registers and reg2 in registers: # [Lists = Parser]
                        reg = reg ^ reg2 # Effects = Interpreter
                        i += 1
                    case ["ora", reg, reg2] if reg in registers and reg2 in registers:
                        reg = reg | reg2
                        i += 1
                    case ["prt", reg] if reg in registers:
                        print(registers[reg])
                        i += 1
                    case ["add", val, reg] if reg in registers and val.isnumeric():
                        registers[reg] += int(val)
                        i += 1
                    case ["sar", name]:
                        routines[name] = []
                        i += 1
                    case ["sro", name, *prog] if name in routines:
                        " ".join(prog)
                        routines[name].append(prog)
                        i += 1
                    case ["run", name]:
                        j = i
                        backup = program
                        program = routines[name]
                        interpreter(program)
                    case ["dbg", name] if name in routines:
                        print(routines[name])
            except Exception:
                match instr: # Lexer
                    case ["xor", reg, reg2] if reg in registers and reg2 in registers: # [Lists = Parser]
                        reg = reg ^ reg2 # Effects = Interpreter
                        i += 1
                    case ["ora", reg, reg2] if reg in registers and reg2 in registers:
                        reg = reg | reg2
                        i += 1
                    case ["prt", reg] if reg in registers:
                        print(registers[reg])
                        i += 1
                    case ["add", val, reg] if reg in registers and val.isnumeric():
                        registers[reg] += int(val)
                        i += 1
                    case ["sar", name]:
                        routines[name] = []
                        i += 1
                    case ["sro", name, *prog] if name in routines:
                        " ".join(prog)
                        routines[name].append(prog)
                        i += 1
                    case ["run", name]:
                        j = i
                        backup = program
                        program = routines[name]
                        interpreter(program)
                    case ["dbg", name] if name in routines:
                        print(routines[name])

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
        elif userinput == "/erase":
            program = []
        elif userinput == "/program":
            print(program)
        elif userinput == "/diskwipe":
            backup = []
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
