import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens

precedence = (
    ("right", 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'ASSIGN'),
    ("nonassoc", 'LESS', 'GREATER', 'LESSEQ', 'GREATEREQ'),
    ("nonassoc", 'INEQ', 'EQ'),
    ("left", 'ADD', 'SUB', 'DOTADD', 'DOTSUB'),
    ("left", 'MUL', 'DIV', 'DOTMUL', 'DOTDIV'),
    ("left", 'TRANSPOSE'),
    ("left", 'COMMA')
)

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")
    p[0] = AST.Error()

def p_program(p):
    """program : instructions"""
    p[0] = p[1]

def p_no_instructions(p):
    """instructions : """
    p[0] = AST.InstructionSequence([])

def p_instructions_1(p):
    """instructions : instruction instructions"""
    p[0] = AST.InstructionSequence([p[1]] + p[2].instructions)

def p_instructions_2(p):
    """instructions : instruction_block instructions"""
    p[0] = AST.InstructionSequence([p[1]] + p[2].instructions)

def p_instruction(p):
    """instruction : expression noop
            | if_instruction
            | if_else_instruction
            | while_instruction
            | for_instruction
            | break_instruction
            | continue_instruction
            | return_instruction
            | print_instruction
    """
    p[0] = p[1]

def p_if_else_instruction(p):
    """if_else_instruction : if_instruction else_instruction"""
    p[0] = AST.IfElseExpression(p[1].expr, p[1].if_block, p[2])

def p_if_instruction(p):
    """if_instruction : IF paren_expression instruction
                      | IF paren_expression instruction_block"""
    p[0] = AST.IfElseExpression(p[2], p[3])

def p_else_instruction(p):
    """else_instruction : ELSE instruction
                      | ELSE instruction_block"""
    p[0] = p[2]

def p_while_instruction(p):
    """while_instruction : WHILE paren_expression instruction
                         | WHILE paren_expression instruction_block"""
    p[0] = AST.WhileExpression(p[2], p[3])

def p_for_instruction(p):
    """for_instruction : FOR identifier ASSIGN range instruction
                       | FOR identifier ASSIGN range instruction_block"""
    p[0] = AST.ForExpression(p[2], p[4], p[5])

def p_break_instruction(p):
    """break_instruction : BREAK noop"""
    p[0] = AST.BreakInstruction()

def p_continue_instruction(p):
    """continue_instruction : CONTINUE noop"""
    p[0] = AST.ContinueInstruction()

def p_print_instruction(p):
    """print_instruction : PRINT print_args noop"""
    p[0] = AST.PrintInstruction(p[2])

def p_print_args_1(p):
    """print_args : expression"""
    p[0] = [p[1]]

def p_print_args_2(p):
    """print_args : expression COMMA print_args"""
    p[0] = [p[1]] + p[3]

def p_return_instruction(p):
    """return_instruction : RETURN expression noop"""
    p[0] = AST.ReturnInstruction(p[2])

def p_instruction_block(p):
    """instruction_block : LCPAREN instructions RCPAREN"""
    p[0] = p[2]

def p_expression(p):
    """expression : binary_operation
          | unary_operation
          | identifier
          | constant
          | initializer
          | subscript
          | paren_expression
    """
    p[0] = p[1]

def p_paren_expression(p):
    """paren_expression : LPAREN expression RPAREN"""
    p[0] = p[2]

def p_binary_operation(p):
    """binary_operation : expression ADD expression
                | expression SUB expression
                | expression MUL expression
                | expression DIV expression
                | expression DOTADD expression
                | expression DOTSUB expression
                | expression DOTMUL expression
                | expression DOTDIV expression
                | expression ADDASSIGN expression
                | expression SUBASSIGN expression
                | expression MULASSIGN expression
                | expression DIVASSIGN expression
                | expression ASSIGN expression
                | expression LESS expression
                | expression GREATER expression
                | expression LESSEQ expression
                | expression GREATEREQ expression
                | expression EQ expression
                | expression INEQ expression
                | range
    """
    p[0] = AST.BinaryExpression(p[2], p[1], p[3])

def p_range(p):
    """range : expression RANGE expression"""
    p[0] = AST.BinaryExpression(p[2], p[1], p[3])

def p_unary_operation(p):
    """unary_operation : left_unary_operation
               | right_unary_operation
    """
    p[0] = p[1]

def p_left_unary_operation(p):
    """left_unary_operation : SUB expression"""
    p[0] = AST.LeftUnaryExpression(p[1], p[2])

def p_right_unary_operation(p):
    """right_unary_operation : expression TRANSPOSE"""
    p[0] = AST.RightUnaryExpression(p[2], p[1])

def p_identifier(p):
    """identifier : ID"""
    p[0] = AST.Variable(p[1])

def p_constant(p):
    """constant : integer_constant
                | floating_constant
                | string_constant"""
    p[0] = p[1]

def p_integer_constant(p):
    """integer_constant : INTEGER"""
    p[0] = AST.Integer(p[1])

def p_floating_constant(p):
    """floating_constant : FLOATING"""
    p[0] = AST.Float(p[1])

def p_string_constant(p):
    """string_constant : STRING"""
    p[0] = AST.String(p[1])

def p_initializer(p):
    """initializer : special_function
           | array
    """
    p[0] = p[1]

def p_array(p):
    """array : LSQPAREN array_initialization RSQPAREN"""
    p[0] = AST.Array(p[2])

def p_array_initialization_1(p):
    """array_initialization : """
    p[0] = []

def p_array_initialization_2(p):
    """array_initialization : expression"""
    p[0] = [p[1]]

def p_array_initialization_3(p):
    """array_initialization : expression COMMA array_initialization"""
    p[0] = [p[1]] + p[3]

def p_special_function(p):
    """special_function : ones_function
               | zeros_function
               | eye_function
        """
    p[0] = p[1]

def p_ones_function1(p):
    """ones_function : ONES LPAREN expression RPAREN"""
    p[0] = AST.SpecialFunction(p[1], p[3])

def p_ones_function2(p):
    """ones_function : ONES LPAREN expression COMMA expression RPAREN"""
    p[0] = AST.SpecialFunction(p[1], p[3], p[5])

def p_zeros_function1(p):
    """zeros_function : ZEROS LPAREN expression RPAREN"""
    p[0] = AST.SpecialFunction(p[1], p[3])

def p_zeros_function2(p):
    """zeros_function : ZEROS LPAREN expression COMMA expression RPAREN"""
    p[0] = AST.SpecialFunction(p[1], p[3], p[5])

def p_eye_function1(p):
    """eye_function : EYE LPAREN expression RPAREN"""
    p[0] = AST.SpecialFunction(p[1], p[3])

def p_eye_function2(p):
    """eye_function : EYE LPAREN expression COMMA expression RPAREN"""
    p[0] = AST.SpecialFunction(p[1], p[3], p[5])

def p_subscript(p):
    """subscript : expression LSQPAREN expression RSQPAREN"""
    p[0] = AST.BinaryExpression("[]", p[1], p[3])

def p_2D_subscript(p):
    """subscript : expression LSQPAREN expression COMMA expression RSQPAREN"""
    p[0] = AST.BinaryExpression("[]", p[1], AST.Pair(p[3], p[5]))

def p_noop(p):
    """noop : SEMICOLON"""

parser = yacc.yacc()