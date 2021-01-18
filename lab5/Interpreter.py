
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)


op_dict = {
    
}

class Interpreter(object):
    def interprete(self, ast):
        print("pooopa1")
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
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        print(r1)
        print(r2)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

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

