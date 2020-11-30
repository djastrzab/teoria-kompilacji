

class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class IntNum(Node):
    def __init__(self, value):
        self.value = value
        self.type = "IntNum"

class FloatNum(Node):

    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class MatWord(Node):
    def __init__(self, word, value):
        self.word = word
        self.value = value

class ReturnStatement(Node):
    def __init__(self, word, value=None):
        self.word = word
        self.value = value


# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass
      