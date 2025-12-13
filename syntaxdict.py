draft = []

syntax = {
    "if": "if",
    "then": ":\n    ",
    "end": "\n",
    "true": "True"
}

userinput = input().split()
for item in userinput:
    if item in syntax:
        item = syntax[item]
        draft.append(item)
    else:
        draft.append(item)

code = " ".join(draft)
final = f"""{code}"""
print(final)
exec(final)