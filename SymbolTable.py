class VariableSymbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class SymbolTable(object):

    def __init__(self, parent, name):
        self.parent_scope = parent
        self.scope_name = name
        self.symbols = {}
        self.child_scope = None

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent_scope is not None:
            return self.parent_scope.get(name)
        else:
            return None

    def getParentScope(self):
        return self.parent_scope

    def pushScope(self, name):
        self.child_scope = SymbolTable(self, name)
        return self.child_scope

    def popScope(self):
        if self.parent_scope is not None:
            self.parent_scope.child_scope = None
            return self.parent_scope
        return None