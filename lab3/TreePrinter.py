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
        self.left.printTree()
        self.right.printTree()

        #raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        # print(self.type,self.value)
        print("| " * indent + str(self.value))
        #pass
        # fill in the body

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


    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass    
        # fill in the body


    # define printTree for other classes
    # ...

