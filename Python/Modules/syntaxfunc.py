draft = []

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
            draft.append(item)
