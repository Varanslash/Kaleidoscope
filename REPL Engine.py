variables = {}
error = "error"

while True:  # Loop
    userinput = input().split()
    match userinput:
        case ["set", var, value]:  # Read
            try:  # Eval
                variables[var] = int(value)
            except Exception:
                print(error)