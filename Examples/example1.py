import tokenfunctions
tokenfunctions.error("invalid symbol")
tokenfunctions.define(">", """print("hi")""")
tokenfunctions.interpreter("> > > > >")
