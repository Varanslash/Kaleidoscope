 # Imports (for controlling the processor)

import sys
import time
import math
import json

# Memory

filename = "Downloads/extprocessor.aminus"
program = []
backendmemory = list(range(65536))
memory = [hex(num) for num in backendmemory]
stack = [0] * 65535
routines = {}
loops = {}
registers = {
    
}
flags = {

}
stacks = {

}
banks = {

}
i = 0
j = 0
log = []

start = {}
end = {}

lstart = {}
lend = {}

ifstart = {}
elsestart = {}
ifend = {}

# Function Call Frames

jstack = []
fnstack = []

# Loop Call Frames

lstack = []
lvalstack = []

# Fancy name for computer storage

sram = {
    "currentfn": " "
}

# when i get high on water

JumpInterrupt = False
RoutInterrupt = False # yes, you
loopvalue = 0

# General Processor

def index(program):
    n = 0
    for index in program:
        match index.split():
            case ["fn", name]:
                start[name] = n
                n += 1
            case ["end", "fn", name]:
                end[name] = n
                n += 1
            case ["loop", name, flag, value]:
                lstart[name] = n
                n += 1
            case ["end", "loop", name]:
                lend[name] = n
                n += 1
            case ["if", flag, name]:
                ifstart[name] = n
                n += 1
            case ["else", flag, name]:
                elsestart[name] = n
                n += 1
            case ["end", "if", flag, name]:
                ifend[name] = n
                n += 1
            case _:
                n += 1

def interpreter(program):
    global RoutInterrupt, JumpInterrupt, loopvalue
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

            # I/O

            case ["sprt", *string]:
                print(*string)
                i += 1
            case ["input", reg, string]:
                registers[reg] = input(string)
                i += 1 

            # Variables

            case ["var", "int", reg] if reg not in registers:
                registers[reg] = 0
                i += 1
            case ["set", "var", reg, val] if reg in registers and val.isnumeric():
                registers[reg] = int(val)
                i += 1
            case ["var", "stack", reg] if reg not in stacks:
                stacks[reg] = []
                i += 1
            case ["append", "stack", reg, val] if reg in stacks:
                if val.isnumeric():
                    stacks[reg].append(int(val))
                elif val in ["True", "False"]:
                    if val == "True":
                        stacks[reg].append(val == True)
                    else:
                        stacks[reg].append(val == False)
                else:
                    stacks[reg].append(val)
                i += 1
            case ["pop", "stack", reg, idx] if reg in stacks:
                stacks[reg].pop(int(idx))
                i += 1
            case ["var", "bank", reg] if reg not in banks:
                banks[reg] = {}
                i += 1
            case ["key", "bank", reg, key, val] if reg in banks:
                if val.isnumeric():
                    banks[reg][key] = int(val)
                elif val in ["True", "False"]:
                    if val == "True":
                        banks[reg][key] = val = True
                    else:
                        banks[reg][key] = val = False
                else:
                    banks[reg][key] = val
                i += 1

            # Bitwise Logic

            case ["xor", reg, reg2] if reg in registers and reg2 in registers:
                registers[reg] = registers[reg] ^ registers[reg2]
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

            # More I/O

            case ["rprt", reg] if reg in registers:
                print(registers[reg])
                i += 1

            # Arithmetic

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
                i += 1

            # Functions

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

            # Control Flow

            case ["jmp", idx]:
                i = idx 
            case ["return"]:
                i = len(program)
            case ["%", *string]:
                i += 1

            # Flags

            case ["reg", "flag", name] if name not in flags:
                flags[name] = False
                i += 1
            case ["set", "flag", name, stat] if name in flags and stat in ["True", "False"]:
                flags[name] = True if stat == "True" else False
                i += 1

            # Loops

            case ["loop", name, flag, value]:
                if flags[flag] == True:
                    try:
                        lvalstack.pop(-1)
                        lvalstack.append(loopvalue)
                    except Exception:
                        pass
                    loopvalue = int(value)
                    lvalstack.append(loopvalue)
                    i += 1
                else:
                    i = lend[name] + 1
            case ["end", "loop", flag, name]:
                if flags[flag] == False or loopvalue <= 0:
                    lvalstack.pop(-1)
                    try:
                        loopvalue = lvalstack[-1]
                    except IndexError:
                        pass
                    i += 1
                else:
                    loopvalue -= 1
                    i = lstart[name] + 1

            # If/Else/End

            case ["if", flag, name]:
                if flags[flag] == True:
                    i += 1
                else:
                    i = elsestart[name] + 1
            case ["else", flag, name]:
                if flags[flag] == False:
                    i += 1
                else:
                    i = ifend[name] + 1
            case ["end", "if", flag, name]:
                i += 1

# Text Editor

try:
    with open(filename, "r") as macro:
        program = json.load(macro)
        for line in program:
            print(line)
except FileNotFoundError:
    print("No program found")

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
        elif userinput == "/index":
            index(program)
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