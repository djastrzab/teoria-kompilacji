
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)




class Interpreter(object):
    op_dict = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        "+=": lambda x, y: self.scopes.set(x, x + y),
        "-=": lambda x, y: self.scopes.set(x, x - y),
        "*=": lambda x, y: self.scopes.set(x, x * y),
        "/=": lambda x, y: self.scopes.set(x, x / y)
    }


    def __init__(self):
        self.scopes = MemoryStack()

    def interprete(self, ast):
        print("pooopa1")
        self.scopes.push(Memory("global"))
        self.visit(ast)

    @on('node')
    def visit(self, node):
        print("pooopa0")
        pass

    @when(AST.Node)
    def visit(self, node):
        print("pooopa2")
        self.visit(node.left)
        self.visit(node.right)
    

    @when(AST.BinExpr)
    def visit(self, node):
        print("pooopa3")
        print(node.op)
        r2 = self.visit(node.right)
        if node.op == '=':
            self.scopes.insert(node.left.name, r2)
            return r2
        r1 = self.visit(node.left)
        return op_dict[node.op](r1, r2)

    @when(AST.Variable)
    def visit(self, node):
        return self.scopes.get(node.name)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.string

    @when(AST.Printable)
    def visit(self, node):
        return self.visit(node.printable)

    @when(AST.PrintStatement)
    def visit(self, node):
        text = ""
        for printable in node.content:
            r = self.visit(printable)
            text += str(r) + " "
        print(text)
        return None

    # @when(AST.Assignment)
    # def visit(self, node):
    #     a = 1
    #
    #

    # simplistic while loop interpretation
    @when(AST.WhileLoop)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

