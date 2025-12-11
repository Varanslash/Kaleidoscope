syntax = {

}

def error(string):
    global errormessage
    errormessage = string

def define(char, code):
    syntax[char] = code

def interpreter(program):
    global finalizedprogram
    finalizedprogram = program.split()
    for token in finalizedprogram:
        if token not in syntax:
            print(errormessage)
        else:
            exec(str(syntax[token]))