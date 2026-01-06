 # Imports (for controlling the processor)

import sys
import time
import math
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
        instr = program[i]
        for instr in program:
            match instr.split(): # Lexer
                case ["xor", reg, reg2] if reg in registers and reg2 in registers: # [Lists = Parser]
                    registers[reg] = registers[reg] ^ registers[reg2] # Effects = Interpreter
                    i += 1
                case ["ora", reg, reg2] if reg in registers and reg2 in registers:
                    registers[reg] = registers[reg] | registers[reg2]
                    i += 1
                case ["not", reg] if reg in registers:
                    registers[reg] = ~registers[reg]
                    i += 1
                case ["and", reg, reg2] if reg in registers and reg2 in registers:
                    registers[reg] = registers[reg] & registers[reg2]
                    i += 1
                case ["prt", reg] if reg in registers:
                    print(registers[reg])
                    i += 1
                case ["add", reg, val] if reg in registers and val.isnumeric():
                    registers[reg] += int(val)
                    i += 1
                case ["sub", reg, val] if reg in registers and val.isnumeric():
                    registers[reg] -= int(val)
                    i += 1
                case ["mul", reg, val] if reg in registers and val.isnumeric():
                    registers[reg] *= int(val)
                    i += 1
                case ["div", reg, val] if reg in registers and val.isnumeric():
                    registers[reg] /= int(val)
                    i += 1
                case ["inc", reg] if reg in registers and val.isnumeric():
                    registers[reg] += 1
                    i += 1
                case ["dec", reg] if reg in registers and val.isnumeric():
                    registers[reg] -= 1
                    i += 1
                case ["bsl", reg, val] if reg in registers and val.isnumeric():
                    registers[reg] <<= int(val)
                    i += 1
                case ["bsr", reg, val] if reg in registers and val.isnumeric():
                    registers[reg] >>= int(val)
                    i += 1
                case ["mod", reg, val] if reg in registers and val.isnumeric():
                    registers[reg] %= int(val)
                    i += 1
                case ["fac", reg, dest] if reg in registers and dest in registers:
                    registers[dest] = math.factorial(registers[reg])
                case ["sar", name]:
                    routines[name] = []
                    i += 1
                case ["sro", name, *prog] if name in routines:
                    routines[name].append(" ".join(prog))
                    i += 1
                case ["run", name]:
                    j = i
                    backup = program
                    program = routines[name]
                    interpreter(program)
                case ["lup", name, val]:
                    j = i
                    backup = program
                    program = routines[name]
                    for _ in range(int(val)):
                        interpreter(program)

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
