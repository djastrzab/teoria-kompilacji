

class Node:
    def __init__(self, left, right, line_no=None):
        self.left = left
        self.right = right
        self.line_no = line_no


class IntNum(Node):
    def __init__(self, value, line_no=None):
        self.value = value
        self.line_no = line_no

class Scope(Node):
    def __init__(self, instructions, line_no=None):
        self.instructions = instructions
        self.line_no = line_no

class FloatNum(Node):
    def __init__(self, value, line_no=None):
        self.value = value
        self.line_no = line_no

class String(Node):
    def __init__(self, string, line_no=None):
        self.string = string
        self.line_no = line_no

class Printable(Node):
    def __init__(self, printable, line_no=None):
        self.printable = printable
        self.line_no = line_no

class Variable(Node):
    def __init__(self, name, line_no=None):
        self.name = name
        self.line_no = line_no


class BinExpr(Node):
    def __init__(self, op, left, right, line_no=None):
        self.op = op
        self.left = left
        self.right = right
        self.line_no = line_no

class MatWord(Node):
    def __init__(self, word, value, line_no=None):
        self.word = word
        self.value = value
        self.line_no = line_no

class ReturnStatement(Node):
    def __init__(self, word, value=None, line_no=None):
        self.word = word
        self.value = value
        self.line_no = line_no

class PrintStatement(Node):
    def __init__(self, content, line_no=None):
        self.content = content    # now a list
        self.line_no = line_no

class UnaryMinus(Node):
    def __init__(self, expr, line_no=None):
        self.expr = expr
        self.line_no = line_no

class UnaryTranspose(Node):
    def __init__(self, expr, line_no=None):
        self.expr = expr
        self.line_no = line_no

class ForLoop(Node):
    def __init__(self, var, _range, block, line_no=None):
        self.var = var
        self._range = _range
        self.block = block
        self.line_no = line_no

class WhileLoop(Node):
    def __init__(self, condition, operations, line_no=None):
        self.condition = condition
        self.operations = operations
        self.line_no = line_no

class IfElse(Node):
    def __init__(self, condition, ifBlock, elseBlock=None, line_no=None):
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock
        self.line_no = line_no

class Matrix(Node):
    def __init__(self, rows, line_no=None):
        self.rows = rows
        self.line_no = line_no

class Vector(Node):
    def __init__(self, inside, line_no=None):
        self.inside = inside
        self.line_no = line_no


class BreakInstruction(Node):
    def __init__(self, line_no=None):
        self.line_no = line_no
        pass

class ContinueInstruction(Node):
    def __init__(self, line_no=None):
        self.line_no = line_no
        pass

class Error(Node):
    def __init__(self, line_no=None):
        self.line_no = line_no
        pass
      