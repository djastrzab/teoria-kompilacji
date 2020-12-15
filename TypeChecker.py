import AST
from SymbolTable import SymbolTable
from Types import OpType, Matrix, Array, String, Float, Int, tarray, Pair, tfloat, tmatrix, tint, Variable, tvariable, \
    tpair, Range, trange


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

class TypeChecker(NodeVisitor):

    def __init__(self):
        self.current_scope = SymbolTable(None, "global")
        self.optype = OpType()

    def common(self, v1, v2):
        if v1 is not None and v2 is not None:
            return (v1 == v2, v1)
        else:
            return (True, None)

    def visit_Pair(self, node):
        type1 = self.visit(node.v1)
        type2 = self.visit(node.v2)
        if type1 != type2 or type1 != tint:
            print("2D index must be integral!")
        return Pair(type1, type1.get_constant(), type2.get_constant())

    def visit_LeftUnaryExpression(self, node):
        type = self.visit(node.subop)
        op = node.op
        if type == tvariable:
            type = type.type

        return type

    def visit_RightUnaryExpression(self, node):
        type = self.visit(node.subop)
        op = node.op
        if type is not None:
            if type == tvariable:
                type = type.type
                if type is None:
                    print("Variable with no type!")
                return type
            if type != tmatrix:
                print("Transposition can be only performed on matrix!")

        return type

    def visit_BinaryExpression(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)

        op = node.op

        if type1 is None or type2 is None:
            print("Invalid operands for {}!".format(op))
        else:
            if op == '=' and type1 == tvariable:
                if type2 == tvariable:
                    type2 = type2.type
                type1.type = type2
                type1 = type1.type
                return type1
            else:
                if type1 == tvariable:
                    type1 = type1.type
                if type2 == tvariable:
                    type2 = type2.type
            if type1 is not None and type2 is not None:
                if type1 == tmatrix and type2 == tmatrix:
                    common_subtype = self.optype.getOpType(op, type1.subtype(), type2.subtype())
                    if common_subtype is not None:
                        if op in ['+', '-', '.+', '.-', '.*', './', '+=', '-=']:
                            checks = [self.common(type1.rows(), type2.rows()), self.common(type1.cols(), type2.cols())]
                            if all(map(lambda x: x[0], checks)):
                                is_const = all(map(lambda x: x[1] is not None, checks))
                                return Matrix(common_subtype, type1.rows() if is_const else None,
                                              type1.cols() if is_const else None)
                            else:
                                print("Invalid operands for {}!".format(op))
                        elif op == '*':
                            checks = [self.common(type1.cols(), type2.rows())]
                            if all(map(lambda x: x[0], checks)):
                                is_const = all(map(lambda x: x[1] is not None, checks))
                                return Matrix(common_subtype, type1.rows() if is_const else None,
                                              type2.cols() if is_const else None)
                            else:
                                print("Invalid operands for {}!".format(op))
                        elif op == '*=':
                            checks = [self.common(type1.rows(), type2.rows()), self.common(type1.cols(), type2.cols()),
                                      self.common(type1.cols(), type2.rows())]
                            if all(map(lambda x: x[0], checks)):
                                is_const = all(map(lambda x: x[1] is not None, checks))
                                return Matrix(type1.subtype(), type1.rows() if is_const else None,
                                              type1.cols() if is_const else None)
                            else:
                                print("Invalid operands for {}!".format(op))
                        else:
                            print("Invalid operands for {}!".format(op))
                    else:
                        print("Invalid operands for {}!".format(op))
                elif type1 == tmatrix and type2 == tarray:
                    common_subtype = self.optype.getOpType(op, type1.subtype(), type2.subtype())
                    if common_subtype is not None:
                        if op == '*':
                            checks = [self.common(type1.cols(), type2.length())]
                            if all(map(lambda x: x[0], checks)):
                                is_const = all(map(lambda x: x[1] is not None, checks))
                                return Array(common_subtype, type1.rows() if is_const else None)
                            else:
                                print("Invalid operands for {}!".format(op))
                elif type1 == tarray and type2 == tmatrix:
                    common_subtype = self.optype.getOpType(op, type1.subtype(), type2.subtype())
                    if common_subtype is not None:
                        if op == '*':
                            checks = [self.common(type1.length(), type2.rows())]
                            if all(map(lambda x: x[0], checks)):
                                is_const = all(map(lambda x: x[1] is not None, checks))
                                return Array(common_subtype, type1.cols() if is_const else None)
                            else:
                                print("Invalid operands for {}!".format(op))
                elif type1 == tarray and type2 == tarray:
                    if op in ['.+', '.-', '.*', './']:
                        common_subtype = self.optype.getOpType(op, type1.subtype(), type2.subtype())
                        if common_subtype is not None:
                            checks = [self.common(type1.length(), type2.length())]
                            if all(map(lambda x: x[0], checks)):
                                is_const = all(map(lambda x: x[1] is not None, checks))
                                return Array(common_subtype, type1.length() if is_const else None)
                            else:
                                print("Invalid operands for {}!".format(op))
                        else:
                            print("Invalid operands for {}!".format(op))
                    else:
                        common_subtype = self.optype.getOpType(op, type1, type2)
                        if common_subtype is not None:
                            is_const = type1.length() is not None and type2.length() is not None
                            return Array(common_subtype, type1.length() + type2.length() if is_const else None)
                        else:
                            print("Invalid operands for {}!".format(op))
                elif type1 == tarray and type2 == tint and op == '[]':
                    if type1.length() is not None and type2.is_constant():
                        if type2.get_constant() >= type1.length():
                            print("Invalid operands for {}!".format(op))
                    return type1.subtype()
                elif type1 == tmatrix and type2 == tpair and op == '[]':
                    if type1.rows() is not None and type1.cols() is not None and type2.is_constant():
                        if type2.get_constant()[0] >= type1.rows() or type2.get_constant()[1] >= type1.cols():
                            print("Invalid operands for {}!".format(op))
                    return type1.subtype()
                elif type1 == tint and type2 == tint and op == ':':
                    return Range(tint)
                else:
                    result_type = self.optype.getOpType(op, type1, type2)
                    if result_type is None:
                        print("Invalid operands for {}!".format(op))
            else:
                print("Invalid operands for {}!".format(op))

        return None

    def visit_Integer(self, node):
        return Int(node.value)

    def visit_Float(self, node):
        return Float(node.value)

    def visit_String(self, node):
        return String(node.value)

    def visit_InstructionSequence(self, node):
        self.current_scope = self.current_scope.pushScope("while loop")
        for instruction in node.instructions:
            self.visit(instruction)
        self.current_scope = self.current_scope.popScope()

    def visit_WhileExpression(self, node):

        result = self.visit(node.expr)
        if result is None or result != tint:
            print("While condition must evaluate to int!")

        self.current_scope = self.current_scope.pushScope("while loop")

        self.current_scope.put('for while', 'loop')

        return None

    def visit_ForExpression(self, node):
        self.current_scope = self.current_scope.pushScope("for loop")

        self.current_scope.put('for while', 'loop')
        self.current_scope.put(node.variable.name, self.visit(node.variable))
        result = self.visit(node.range)
        if result is None or result != trange:
            print("For range is invalid!")
        else:
            if result.subtype() != tint:
                print("For range must be integer range!")

        self.visit(node.for_block)

        self.current_scope = self.current_scope.popScope()

        return None

    def visit_PrintInstruction(self, node):
        for arg in node.args:
            self.visit(arg)

    def visit_IfElseExpression(self, node):

        result = self.visit(node.expr)
        if result is None or result != tint:
            print("For range is invalid!")

        self.current_scope = self.current_scope.pushScope("if")
        self.visit(node.if_block)
        self.current_scope = self.current_scope.popScope()

        if node.else_block is not None:
            self.current_scope = self.current_scope.pushScope("else")
            self.visit(node.else_block)
            self.current_scope = self.current_scope.popScope()

        return None

    def visit_BreakInstruction(self, node):
        if self.current_scope.get('for while') is None:
            print("Break instruction not in loop!")
        return None

    def visit_ContinueInstruction(self, node):
        if self.current_scope.get('for while') is None:
            print("Continue instruction not in loop!")
        return None

    def visit_ReturnInstruction(self, node):
        self.visit(node.expr)
        return None

    def visit_Array(self, node):
        # check if matrix
        sublen = None
        subtype = None
        for element in node.elements:
            result = self.visit(element)
            if result == tarray: # if potential matrix
                if sublen is None:
                    sublen = result.length()
                    subtype = result.subtype()
                elif sublen != result.length() or not result.subtype().convertible_to(subtype):
                    print("Matrix initialization requires subarrays to be of equal size and same type!")
                    break
            else: # 1D array
                if sublen is not None:
                    print("Matrix initialization requires subarrays to be of equal size and same type!")
                    break
                if subtype is None:
                    subtype = result
                elif not result.convertible_to(subtype):
                    print("Array initialization requires same types!")
                    break
        if sublen is not None:
            return Matrix(subtype, len(node.elements), sublen)
        else:
            return Array(subtype, len(node.elements))

    def visit_SpecialFunction(self, node):
        arg0 = self.visit(node.arg0)
        if arg0 is None or arg0 != tint:
            print("eye, zeroes, ones require int argument!")

        if node.arg1 is not None:
            arg1 = self.visit(node.arg1)
            if arg1 is None or arg1 != tint:
                print("eye, zeroes, ones require int argument!")
            return Matrix(tfloat, arg0.get_constant(), arg1.get_constant())
        else:
            return Matrix(tfloat, arg0.get_constant(), arg0.get_constant())

    def visit_Variable(self, node):
        var = self.current_scope.get(node.name)
        if var is None:
            self.current_scope.put(node.name, Variable(node.name))
        return self.current_scope.get(node.name)


