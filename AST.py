from dataclasses import dataclass

@dataclass
class Node(object):
    def __init__(self, line, pos):
        self.line = line
        self.pos = pos

@dataclass
class Integer(Node):
    def __init__(self, value):
        self.value = value

@dataclass
class Float(Node):
    def __init__(self, value):
        self.value = value

@dataclass
class String(Node):
    def __init__(self, value):
        self.value = value

@dataclass
class Pair(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

@dataclass
class Variable(Node):
    def __init__(self, name):
        self.name = name

@dataclass
class LeftUnaryExpression(Node):
    def __init__(self, op, subop):
        self.op = op
        self.subop = subop

@dataclass
class RightUnaryExpression(Node):
    def __init__(self, op, subop):
        self.op = op
        self.subop = subop

@dataclass
class BinaryExpression(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

@dataclass
class IfElseExpression(Node):
    def __init__(self, expr, if_block, else_block = None):
        self.expr = expr
        self.if_block = if_block
        self.else_block = else_block

@dataclass
class WhileExpression(Node):
    def __init__(self, expr, while_block):
        self.expr = expr
        self.while_block = while_block

@dataclass
class ForExpression(Node):
    def __init__(self, variable, range, for_block):
        self.variable = variable
        self.range = range
        self.for_block = for_block

@dataclass
class InstructionSequence(Node):
    def __init__(self, instructions):
        self.instructions = instructions

@dataclass
class BreakInstruction(Node):
    def __init__(self):
        pass

@dataclass
class ContinueInstruction(Node):
    def __init__(self):
        pass

@dataclass
class ReturnInstruction(Node):
    def __init__(self, expr):
        self.expr = expr

@dataclass
class PrintInstruction(Node):
    def __init__(self, args):
        self.args = args

@dataclass
class Array(Node):
    def __init__(self, elements):
        self.elements = elements

@dataclass
class SpecialFunction(Node):
    def __init__(self, name, arg0, arg1 = None):
        self.name = name
        self.arg0 = arg0
        self.arg1 = arg1

@dataclass
class Noop(Node):
    def __init__(self, noop):
        self.noop = noop

@dataclass
class Error(Node):
    def __init__(self):
        pass