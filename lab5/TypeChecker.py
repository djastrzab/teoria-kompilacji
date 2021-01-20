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
ttype[".+"]["int"]["int"] = "int"
ttype[".-"]["int"]["int"] = "int"
ttype[".*"]["int"]["int"] = "int"
ttype["./"]["int"]["int"] = "int"
ttype['<']["int"]["int"] = "logic"
ttype['>']["int"]["int"] = "logic"
ttype["<="]["int"]["int"] = "logic"
ttype[">="]["int"]["int"] = "logic"
ttype["=="]["int"]["int"] = "logic"
ttype["!="]["int"]["int"] = "logic"
ttype[':']["int"]["int"] = "int"

ttype['+']["int"]["float"] = "float"
ttype['-']["int"]["float"] = "float"
ttype['*']["int"]["float"] = "float"
ttype['/']["int"]["float"] = "float"
ttype[".+"]["int"]["float"] = "float"
ttype[".-"]["int"]["float"] = "float"
ttype[".*"]["int"]["float"] = "float"
ttype["./"]["int"]["float"] = "float"
ttype['<']["int"]["float"] = "logic"
ttype['>']["int"]["float"] = "logic"
ttype["<="]["int"]["float"] = "logic"
ttype[">="]["int"]["float"] = "logic"
ttype["=="]["int"]["float"] = "logic"
ttype["!="]["int"]["float"] = "logic"

ttype['+']["float"]["int"] = "float"
ttype['-']["float"]["int"] = "float"
ttype['*']["float"]["int"] = "float"
ttype['/']["float"]["int"] = "float"
ttype[".+"]["float"]["int"] = "float"
ttype[".-"]["float"]["int"] = "float"
ttype[".*"]["float"]["int"] = "float"
ttype["./"]["float"]["int"] = "float"
ttype['<']["float"]["int"] = "logic"
ttype['>']["float"]["int"] = "logic"
ttype["<="]["float"]["int"] = "logic"
ttype[">="]["float"]["int"] = "logic"
ttype["=="]["float"]["int"] = "logic"
ttype["!="]["float"]["int"] = "logic"

ttype['+']["float"]["float"] = "float"
ttype['-']["float"]["float"] = "float"
ttype['*']["float"]["float"] = "float"
ttype['/']["float"]["float"] = "float"
ttype[".+"]["float"]["float"] = "float"
ttype[".-"]["float"]["float"] = "float"
ttype[".*"]["float"]["float"] = "float"
ttype["./"]["float"]["float"] = "float"
ttype['<']["float"]["float"] = "logic"
ttype['>']["float"]["float"] = "logic"
ttype["<="]["float"]["float"] = "logic"
ttype[">="]["float"]["float"] = "logic"
ttype["=="]["float"]["float"] = "logic"
ttype["!="]["float"]["float"] = "logic"

ttype['*']["str"]["int"] = "str"


castable_operations = ['/', '+', '-', '*', '>', '<', ">=", "<=", "==", "!="]
castable_matrix_operations = [".+", ".-", ".*", "./"]
castable_types = ["int", "float"]

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
        'diff_ty': "Different types (uncastable)",
        'prev_stage_err': "Error found by parser",
        'no_loop_scope_break': "Break outside loop scope",
        'no_loop_scope_cont': "Continue outside loop scope",
        'ambi_vec_type': "Vector contains different types of elements",
        'ambi_rows_types': "Matrix contains different types of elements",
        'not_eq_rows': "Matrix contains rows of different sizes",
        'not_matrix': "Wrong matrix initialization (empty row or empty matrix)",
        'not_logic': "Not a logical statement",
        'wrong_for_range': "Incorrect for loop range",
        'wrong_trans': "Trying to transpose non-matrix entity",
        'inv_spec_arg': "Wrong matrix size argument",
        'no_var': "Undeclared variable",
        'wr_mat_arg_types': "Wrong types of matrix arguments (not ints)",
        'wr_mat_arg_values': "Wrong values of matrix arguments (outside of matrix)",
        'wr_mat_sizes_op' : "Wrong sizes of matrices in matrix operation",
        'mat_op_on_non_mat' : "Matrix operation on non-matrix arguments"
    }   

    def __init__(self, code, line):
        self.code = code
        self.line = line

    def __str__(self):
        return f'{self.errors[self.code]} in line {self.line}'


class TypeChecker(NodeVisitor):

    def visit_Node(self, node):
        self.visit(node.left)
        self.visit(node.right) 

    def visit_Scope(self, node):
        symtab.pushScope("scope")
        self.visit(node.instructions)
        symtab.popScope()

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        op = node.op
        type2 = self.visit(node.right)
        
        if op == '=':
            if hasattr(node.left, 'op'):
                type1 = self.visit(node.left)
                if type1 != type2:
                    # Error
                    print(Error('diff_ty', node.line_no))
                    return None
                return None
            else:
                if type2:
                    symtab.put(node.left.name, type2)
                return None

        
        if op.find('[,]') != -1:
            var_idx = op.find('[,]')
            type1 = self.visit(node.left)
            var_name = op[:var_idx]
            
            var_type = symtab.get(var_name).type
            if not isinstance(var_type, tuple):
                #error
                print(Error('no_mat_acccess',node.line_no))
                return None
            rows, cols, mat_type = var_type[0], var_type[1], var_type[2]
            if type1 == type2 and type1 == 'int':
                if hasattr(node.left, 'value'):
                    if node.left.value > rows or node.left.value < 0:
                        print(Error('wr_mat_arg_values', node.line_no))
                        return None
                if hasattr(node.right, 'value'):
                    if node.right.value > cols or node.right.value < 0:
                        print(Error('wr_mat_arg_values', node.line_no))
                        return None
                return mat_type
            else:
                print(Error('wr_mat_arg_types', node.line_no))
                return None

        type1 = self.visit(node.left)
        if op in castable_operations and type1 in castable_types and type2 in castable_types:
            return ttype[op][type1][type2]

        if isinstance(type1, tuple) and isinstance(type2, tuple):
            rows1, cols1, vals1 = type1[0], type1[1], type1[2]
            rows2, cols2, vals2 = type2[0], type2[1], type2[2]
            if op == '*':
                if cols1 != rows2:
                    # error
                    print(Error('wr_mat_sizes_op', node.line_no))
                    return None
                if op in ttype and vals1 in ttype[op] and vals2 in ttype[op][vals1]:
                    return (rows1, cols2, ttype[op][vals1][vals2])
                else:
                    # error
                    print(Error('diff_ty', node.line_no))
                    return None
            if not (rows1 == rows2 and cols1 == cols2):
                #error
                print(Error('wr_mat_sizes_op', node.line_no))
                return None
            if not(op in ttype and vals1 in ttype[op] and vals2 in ttype[op][vals1]):
                # error
                print(Error('diff_ty', node.line_no))
                return None
            return (rows1, cols1, ttype[op][vals1][vals2])

        if op in castable_matrix_operations:   # matrix op on non-matrix type
            # error 
            print(Error('mat_op_on_non_mat', node.line_no))
            return None


        if not type1 == 'str':
            if type1 != type2:
                # error
                print(Error('diff_ty', node.line_no))
                return None

        return ttype[op][type1][type2]
        # ...
        #

    def visit_Variable(self, node):
        var = symtab.get(node.name)
        if var:
            return symtab.get(node.name).type
        print(Error('no_var',node.line_no))
        return None

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_String(self, node):
        return "str"

    def visit_Printable(self, node):
        self.visit(node.printable)

    def visit_MatWord(self, node):
        type1 = self.visit(node.value)
        size = node.value.value
        if type1 != "int":
            # error
            print(Error('inv_spec_arg', node.line_no))
        return (size, size, "int")

    def visit_ReturnStatement(self, node):
        if node.value:
            self.visit(node.value)

    def visit_PrintStatement(self, node):
        for c in node.content:
            self.visit(c)

    def visit_UnaryMinus(self, node):
        return self.visit(node.expr)

    def visit_UnaryTranspose(self, node):
        type1 = self.visit(node.expr)
        if not isinstance(type1, tuple):
            # error
            print(Error('wrong_trans', node.line_no))
            pass
        return (type1[1], type1[0], type1[2])

    def visit_ForLoop(self, node):
        type1 = self.visit(node._range)
        if type1 != "int":
            # error
            print(Error('wrong_for_range', node.line_no))
        symtab.put(node.var, type1)
        symtab.pushScope("loop")
        self.visit(node.block)
        symtab.popScope()

    def visit_WhileLoop(self, node):
        type1 = self.visit(node.condition)
        if type1 != "logic":
            # error
            print(Error('not_logic', node.line_no))
        symtab.pushScope("loop")
        self.visit(node.operations)
        symtab.popScope()

    def visit_IfElse(self, node):
        type1 = self.visit(node.condition)
        if type1 != "logic":
            # error
            print(Error('not_logic', node.line_no))
        symtab.pushScope("if")
        self.visit(node.ifBlock)
        symtab.popScope()

        if node.elseBlock:
            symtab.pushScope("else")
            self.visit(node.elseBlock)
            symtab.popScope()

    def visit_Matrix(self, node):     
        rows = len(node.rows)
        row_len = len(node.rows[0].inside)
        if rows < 1 or row_len < 1:
            # ERROR
            print(Error('not_matrix', node.line_no))
            return None
        m_type = self.visit(node.rows[0].inside[0])       # all()
        
        for row in node.rows:
            _, r_len, r_type = self.visit(row)
            if r_len != row_len:
                #ERROR
                print(Error('not_eq_rows', node.line_no))
                return None
            if r_type != m_type:
                #ERROR
                print(Error('ambi_rows_types', node.line_no))
                return None
        return (rows, row_len, m_type)

    def visit_Vector(self, node):
        size = len(node.inside)
        v_type = self.visit(node.inside[0])
        for elem in node.inside:
            type1 = self.visit(elem)
            if v_type != type1:
                #ERROR
                print(Error('ambi_vec_type', node.line_no))
                pass
        return (1, size, v_type)

    def visit_BreakInstruction(self, node):
        loop_scope = symtab.getScope("loop")
        if not loop_scope:
            # ERROR
            print(Error('no_loop_scope_break', node.line_no))
            pass
        
    def visit_ContinueInstruction(self, node):
        loop_scope = symtab.getScope("loop")
        if not loop_scope:
            # ERROR
            print(Error('no_loop_scope_cont', node.line_no))
            pass
    
    def visit_Error(self, node):
        #Error
        print(Error('prev_stage_err', node.line_no))
        pass

## chyba bedzie wypadalo przerobic to na listy zamiast rekurencje bo ciezko sledzic dlugosc rekurencjnego vectora
