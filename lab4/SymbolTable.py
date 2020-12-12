#!/usr/bin/python


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type
    #


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope - ???? and symbol table name
        self.parent = parent
        self.last_scope = -1
        self.scopes = []         # stack of scopes of variables (dicts)
        self.name = name
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.scopes[last_scope][0][name] = VariableSymbol(name, symbol)
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        it = self.last_scope
        while it >= 0:
            if name in self.scopes[it][0]:
                return self.scopes[it][0][name]
            it -= 1
        return None
    #

    def getParentScope(self):
        return self.parent #? ???
    #

    def pushScope(self, name):
        self.scopes.append(({}, name))
        self.last_scope += 1
    #

    def popScope(self):
        self.scopes.pop()
        self.last_scope -= 1
    #

