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
    
}
i = 0
j = 0
log = []
start = {}
end = {}
jstack = []
fnstack = []
sram = {
    "currentfn": " "
}
JumpInterrupt = False
RoutInterrupt = False

# General Processor
def index(program):
    n = 0
    for index in program:
        match index.split(): # Lexer
            case ["fn", name]:
                start[name] = n
                n += 1
            case ["end", "fn", name]:
                end[name] = n
                n += 1
            case _:
                n += 1

def interpreter(program):
    global RoutInterrupt, JumpInterrupt, EndInterrupt
    i = 0
    try:
        if i == log.index(-1) or JumpInterrupt:
            i = j
            program = backup
            JumpInterrupt = False
    except Exception:
        pass
    while i < len(program):
        instr = program[i]
        match instr.split():
            case ["print", string]:
                print(string)
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
            case ["fn", name]:
                if RoutInterrupt == False:
                    i = end[name] + 1
                else:
                    i += 1
            case ["end", "fn", name]:
                if RoutInterrupt == False:
                    i = j
                    JumpInterrupt = True
                else:
                    if sram["currentfn"] == name:
                        j = jstack[-1]
                        i = j
                        jstack.pop()
                        sram["currentfn"] = fnstack[-1]
                        fnstack.pop()
                        RoutInterrupt = False
                        JumpInterrupt = True
                    else:
                        i += 1
            case ["call", "fn", name]:
                j = i + 1
                i = start[name] + 1
                sram["currentfn"] = name
                fnstack.append(name)
                jstack.append(j)
                RoutInterrupt = True
            case ["jmp", idx]:
                i = int(idx)
            case ["return"]:
                i = len(program)

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
                index(program)
                interpreter(program)
        else:
            text = userinput
            program.append(text)

except SystemExit:
    with open(filename, "w") as macro:
        json.dump(program, macro)