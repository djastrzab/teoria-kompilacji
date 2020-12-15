#!/usr/bin/python
from collections import defaultdict

import AST
import SymbolTable

symtab = SymbolTable.SymbolTable(None, "Symtab")

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

ttype['+']["int"]["int"] = "int"
ttype['-']["int"]["int"] = "int"
ttype['*']["int"]["int"] = "int"
ttype['/']["int"]["int"] = "int"
ttype['<']["int"]["int"] = "int"
ttype['>']["int"]["int"] = "int"
ttype["LEQ"]["int"]["int"] = "logic"
ttype["GEQ"]["int"]["int"] = "logic"
ttype["EQ"]["int"]["int"] = "logic"
ttype["NEQ"]["int"]["int"] = "logic"

ttype['+']["int"]["float"] = "float"
ttype['-']["int"]["float"] = "float"
ttype['*']["int"]["float"] = "float"
ttype['/']["int"]["float"] = "float"
ttype["LEQ"]["int"]["float"] = "logic"
ttype["GEQ"]["int"]["float"] = "logic"
ttype["EQ"]["int"]["float"] = "logic"
ttype["NEQ"]["int"]["float"] = "logic"

ttype['+']["float"]["int"] = "float"
ttype['-']["float"]["int"] = "float"
ttype['*']["float"]["int"] = "float"
ttype['/']["float"]["int"] = "float"
ttype["LEQ"]["float"]["int"] = "logic"
ttype["GEQ"]["float"]["int"] = "logic"
ttype["EQ"]["float"]["int"] = "logic"
ttype["NEQ"]["float"]["int"] = "logic"

ttype['+']["float"]["float"] = "float"
ttype['-']["float"]["float"] = "float"
ttype['*']["float"]["float"] = "float"
ttype['/']["float"]["float"] = "float"
ttype["LEQ"]["float"]["float"] = "logic"
ttype["GEQ"]["float"]["float"] = "logic"
ttype["EQ"]["float"]["float"] = "logic"
ttype["NEQ"]["float"]["float"] = "logic"


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class Error:
    errors = {
        'diff_ty': "diffrent Types in line: ",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"}

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.errors[self.code]


class TypeChecker(NodeVisitor):

    def visit_Node(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        op = node.op
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        if op == '=':
            symtab.put(node.left, type2)
            return None
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        if type1 != type2:
            # error
            print(Error('diff_ty'))
            pass

        return ttype[op][type1][type2]
        # ...
        #

    def visit_Variable(self, node):
        return symtab.get(node.name).type if symtab.get(node.name) else None

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_String(self, node):
        return "str"

    def visit_Printable(self, node):
        self.visit(node.printable)
        if node.nxt:
            self.visit(node.nxt)

    def visit_MatWord(self, node):
        type1 = self.visit(node.value)
        if type1 != "int":
            # error
            print("ERROR")

    def visit_ReturnStatement(self, node):
        if node.value:
            self.visit(node.value)

    def visit_PrintStatment(self, node):
        self.visit(node.content)

    def visit_UnaryMinus(self, node):
        return self.visit(node.expr)

    def visit_UnaryMinus(self, node):
        return self.visit(node.expr)

    def visit_UnaryTranspose(self, node):
        type1 = self.visit(node.expr)
        if "mat" not in type1:
            # error
            print("ERROR")

    def visit_ForLoop(self, node):
        type1 = self.visit(node._range)
        if type1 != "int":
            # error
            print("ERROR")
        symtab.put(node.var, type1)
        symtab.pushScope("loop")
        self.visit(node.block)
        symtab.popScope()

    def visit_WhileLoop(self, node):
        type1 = self.visit(node.condition)
        if type1 != "logic":
            # error
            print("ERROR")
        symtab.pushScope("loop")
        self.visit(node.operations)
        symtab.popScope()

    def visit_IfElse(self, node):
        type1 = self.visit(node.condition)
        if type1 != "logic":
            # error
            print("ERROR")
        symtab.pushScope("if")
        self.visit(node.ifBlock)
        symtab.popScope()

        if node.elseBlock:
            symtab.pushScope("else")
            self.visit(node.elseBlock)
            symtab.popScope()

    def visit_Matrix(self, node):
        pass
        ### rekurencja troche problemem

## chyba bedzie wypadalo przerobic to na listy zamiast rekurencje bo ciezko sledzic dlugosc rekurencjnego vectora
