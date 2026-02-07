 # Imports (for controlling the processor)

import sys
import time
import math
import json

# Memory

filename = "extprocessor"
program = []
registers = {
    
}
i = 0
j = 0
log = []
start = {}
end = {}
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
    global RoutInterrupt
    i = 0
    try:
        if i == log.index(-1) or JumpInterrupt:
            i = j
            program = backup
            JumpInterrupt = False
    except Exception:
        pass
    for instr in program:
        match instr.split():
            case ["prt"]:
                print("a") # Lexer
            case ["fn", name]:
                if RoutInterrupt == False:
                    j = end[name] + 1
                    JumpInterrupt = True
                else:
                    i += 1
            case ["end", "fn", name]:
                if RoutInterrupt == False:
                    i = j
                    JumpInterrupt = True
                else:
                    if sram["currentfn"] == name:
                        i = j
                        RoutInterrupt = False
                        JumpInterrupt = True
                    else:
                        i += 1
            case ["call", "fn", name]:
                j = i + 1
                i = start[name] + 1
                sram["currentfn"] = name
                RoutInterrupt = True

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
