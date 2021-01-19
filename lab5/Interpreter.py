import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)


def mul(x ,y):       # can be matrix-multiplication
    return

def mat_add(x, y):
    return 

def mat_sub(x, y):
    return 

def mat_mul(x, y):
    return 

def mat_div(x, y):
    return 
    
def unary_minus(x):  # can be matrix element-wise negation
    return

def mat_el(var,r,c):
    return


# TODO: Need exceptions for variable-based indexes (they are not check in TypeChecker)

def compare(x, y):
    # print(x, "==" ,y)
    # print(x == y)
    return x == y


assign_op_list = ["+=", "-=", "*=", "/="]

class Interpreter(object):
    
    def __init__(self):
        self.scopes = MemoryStack()
        self.op_dict = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': mul,
            '/': lambda x, y: x / y,
            ".+": mat_add,
            ".-": mat_sub,
            ".*": mat_mul,
            "./": mat_div,
            "==": compare,#lambda x, y: x == y,
            "!=": lambda x, y: x != y,
            ">=": lambda x, y: x >= y,
            "<=": lambda x, y: x <= y,
            '<':  lambda x, y: x < y,
            '>':  lambda x, y: x > y,
            "+=": lambda var, x, y: self.scopes.set(var, x + y),
            "-=": lambda var, x, y: self.scopes.set(var, x - y),
            "*=": lambda var, x, y: self.scopes.set(var, x * y),
            "/=": lambda var, x, y: self.scopes.set(var, x / y),
            ":": lambda start, stop: range(start, stop),
            "ZEROES": lambda s: [[0] * s] * s,
            "ONES": lambda s: [[1] * s] * s,
            "EYE": lambda s: [[1 if i == j else 0 for j in range(s)] for i in range(s)],
            "[,]": lambda s,x,y:12312
        }

    def interprete(self, ast):
        #self.scopes.push(Memory("global"))
        self.visit(ast)

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Node)     # TODO: Lists are better, gotta change that
    def visit(self, node):
        self.visit(node.left)
        self.visit(node.right)
    

    @when(AST.BinExpr)
    def visit(self, node):
        # print(node.op)
        r2 = self.visit(node.right)
        if node.op == '=':
            self.scopes.set(node.left.name, r2)
            return r2
        r1 = self.visit(node.left)
        if node.op in assign_op_list:
            return self.op_dict[node.op](node.left.name, r1 ,r2)
        if(node.op.find("[,]")>0):
            trim=node.op.find("[,]")
            return self.scopes.get(node.op[:trim])[r1][r2]
        return self.op_dict[node.op](r1, r2)

    @when(AST.Variable)
    def visit(self, node):
        #print(node.name,"->",self.scopes.get(node.name))
        return self.scopes.get(node.name)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.string[1:-1]

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
        
    @when(AST.Scope)
    def visit(self, node):
        r = None
        try:
            if not node.special:
                self.scopes.push(Memory("Scope"))
            for instruction in node.instructions:
                r = self.visit(instruction)
            if not node.special:
                self.scopes.pop()
        except ReturnValueException as ret:
            ret_val = ret.value
            print(f"Program returned with value: {ret_val}")
            return ret_val
        return r
        
    @when(AST.MatWord)
    def visit(self, node):
        size = self.visit(node.value)
        return self.op_dict[node.word](size)
        
    @when(AST.ReturnStatement)
    def visit(self, node):
        value = self.visit(node.value)
        raise ReturnValueException(value)
        
    @when(AST.UnaryMinus)
    def visit(self, node):
        r = self.visit(node.expr)
        return unary_minus(r)
        
    @when(AST.UnaryTranspose)
    def visit(self, node):
        prev = self.visit(node.expr)
        r = []
        rows = len(r)
        cols = len(r[0])
        for col in range(cols):
            new_row = []
            for row in range(rows):
                new_row.append(prev[row][col])
            r.append(new_row)
        return r
    
    @when(AST.ForLoop)
    def visit(self, node):
        r = None
        iter_list = self.visit(node._range)
        if len(iter_list) > 0:
            self.scopes.push(Memory("ForLoop"))
            node.block.special = True
            self.scopes.insert(node.var, iter_list[0])
            for i in iter_list:
                self.scopes.set(node.var, i)
                try:
                    r = self.visit(node.block)
                    # for mem in self.scopes.mem_stack:
                    #     print(mem.var_dict)
                    # print("---")
                except BreakException:
                    break
                except ContinueException:
                    continue
            dropped_scope = self.scopes.pop()
            while dropped_scope.name != "ForLoop":
                dropped_scope = self.scopes.pop()
            
        return r

    @when(AST.WhileLoop)
    def visit(self, node):
        r = None
        cond = self.visit(node.condition)
        self.scopes.push(Memory("WhileLoop"))
        node.operations.special = True
        while cond:
            try:
                r = self.visit(node.operations)
                cond = self.visit(node.condition)
            except BreakException:
                break
            except ContinueException:
                continue
        dropped_scope = self.scopes.pop()
        while dropped_scope.name != "WhileLoop":
            dropped_scope = self.scopes.pop()
        return r
        
    @when(AST.IfElse)
    def visit(self, node):
        r = None
        cond = self.visit(node.condition)
        node.ifBlock.special = True
        if node.elseBlock:
            node.elseBlock.special = True
        self.scopes.push(Memory("IfElse"))
        if cond:
            r = self.visit(node.ifBlock)
        elif node.elseBlock:
            r = self.visit(node.elseBlock)
        self.scopes.pop()
        
        return r
        
    @when(AST.Matrix)
    def visit(self, node):
        r = []
        for row in node.rows:
            raw_row = self.visit(row)
            r.append(raw_row)
        return r
        
    @when(AST.Vector)
    def visit(self, node):
        r = []
        for val in node.inside:
            raw_val = val.value
            r.append(raw_val)
        return r
        
        
    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()
        
    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()
        
        
    @when(AST.Error)
    def visit(self, node):
        raise Exception(f"Compiling failed on previous part of compilation (error in {node.line_no} line)!")