class Idtk:
    def __init__(self, name, type, returnType=None, paramType=None):
        self.name = name
        self.type = type
        self.retVal = returnType
        self.paramType = paramType



class IdentifierTable:
    def __init__(self):
        self.scopes = [{}]
        self.func = {}

    def enter_func(self,name,type,returnType,paramType=None):
        if name in self.func:
            raise Exception(f"function '{name}' already declared")
        self.func[name] = Idtk(name=name,type=type,returnType=returnType,paramType=paramType)
    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare(self, name, var_type, line):
        if name in self.scopes[-1]:
            raise Exception(f"Variable '{name}' already declared in this scope\nError at line {line}")
        self.scopes[-1][name] = Idtk(name=name,type=var_type)

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name.name in scope:
                return scope[name.name]
        raise Exception(f"Variable '{name.name}' not declared at line {name.line}")
