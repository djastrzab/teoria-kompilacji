from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        if self.left:
            self.left.printTree(indent)
        if self.right:
            self.right.printTree(indent)

        #raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        # print(self.type,self.value)
        print("| " * indent + str(self.value))
        #pass
        # fill in the body

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("| " * indent + self.string)

    @addToClass(AST.PrintStatement)
    def printTree(self, indent=0):
        print("| " * indent + "PRINT")
        self.content.printTree(indent + 1)

    @addToClass(AST.Printable)
    def printTree(self, indent=0):
        self.printable.printTree(indent)
        if self.nxt:
            self.nxt.printTree(indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("| " * indent + self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.MatWord)
    def printTree(self, indent=0):
        print("| " * indent + self.word)
        self.value.printTree(indent + 1)

    @addToClass(AST.ReturnStatement)
    def printTree(self, indent=0):
        print("| " * indent + self.word)
        self.value.printTree(indent + 1)

    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        print("| " * indent + '-')
        self.expr.printTree(indent + 1)

    @addToClass(AST.UnaryTranspose)
    def printTree(self, indent=0):
        print("| " * indent + "TRANSPOSE")
        self.expr.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print("| " * indent + "FOR")
        print("| " * (indent + 1) + self.var)
        self._range.printTree(indent + 1)
        self.block.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print("| " * indent + "WHILE")
        self.condition.printTree(indent + 1)
        self.operations.printTree(indent + 1)

    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.condition.printTree(indent + 1)
        print("| " * indent + "THEN")
        self.ifBlock.printTree(indent + 1)
        print("| " * indent + "ELSE")
        self.elseBlock.printTree(indent + 1)

    @addToClass(AST.BreakInstruction)
    def printTree(self, indent=0):
        print("| " * indent + 'break')

    @addToClass(AST.ContinueInstruction)
    def printTree(self, indent=0):
        print("| " * indent + 'continue')

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print("| " * indent + 'Vector')
        self.inside.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print("| " * indent + 'Vector')
        self.inside.printTree(indent + 1)
        self.deepInside.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass    
        # fill in the body


    # define printTree for other classes
    # ...

