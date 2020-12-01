# !/usr/bin/python

import AST
import scanner
import ply.yacc as yacc

tokens = scanner.tokens
incorrect_input = False
symtab = {}

precedence = (
    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
    ("nonassoc", '=', "ASSIGNPLUS", "ASSIGNMINUS", "ASSIGNTIMES", "ASSIGNDIVIDE"),
    ("nonassoc", '<', '>', "EQ", "NEQ", "LEQ", "GEQ"),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", "\'"),
    ("right", "UNARY"),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        global incorrect_input
        incorrect_input = True
    else:
        print("Unexpected end of input")


def p_start(p):
    """start : 
            | morestatements"""
    p[0] = p[1]


def p_more_statements(p):
    """morestatements : block
                    |  statement morestatements"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST.Node(p[1], p[2])

def p_block(p):
    """block : statement
            | '{' morestatements '}'"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_statement(p):
    """statement : ifstatement
                | loop
                | expr ';'
                | returnstatement ';'
                | assignstatement ';'
                | printstatement ';'
                | BREAK ';'
                | CONTINUE ';'"""
    if p[1] == "break":
        p[0] = AST.BreakInstruction()
    elif p[1] == "continue":
        p[0] = AST.ContinueInstruction()
    else:
        p[0] = p[1]


def p_return_statement(p):
    """returnstatement : RETURN 
                        | RETURN expr"""
    if len(p) == 2:
        p[0] = AST.ReturnStatement(p[1])
    else:
        p[0] = AST.ReturnStatement(p[1], p[2])


def p_print_statement(p):
    """printstatement : PRINT printables"""
    p[0] = AST.PrintStatement(p[2])

def p_printables(p):
    """printables : printable
                | printable ',' printables"""
    if len(p) == 2:
        p[0] = AST.Printable(p[1])
    else:
        p[0] = AST.Printable(p[1], p[3])


def p_pritable1(p):         
    """printable : expr"""
    p[0] = p[1]

def p_pritable2(p):         
    """printable : STRING"""
    p[0] = AST.String(p[1])


def p_assign_statement(p):
    """assignstatement : assignable '=' expr
                        | assignable ASSIGNPLUS expr
                        | assignable ASSIGNMINUS expr
                        | assignable ASSIGNTIMES expr
                        | assignable ASSIGNDIVIDE expr"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_assignable(p):
    """assignable : ID
                    | ID '[' expr ',' expr ']'"""
    if len(p) == 2:
        p[0] = AST.Variable(p[1])
    else:
        p[0] = AST.BinExpr(p[1] + "[,]", p[3], p[5])

def p_expr1(p):
    """expr :  assignable"""
    p[0] = p[1]

def p_expr2(p):
    """expr : INTNUMBER """
    p[0] = AST.IntNum(p[1])

def p_expr3(p):  
    """expr : FLOATNUMBER"""
    p[0] = AST.FloatNum(p[1])

def p_expr4(p):
    """expr : '-' expr %prec UNARY
            | expr "\'"
            | specialmatrixword '(' expr ')'
            | '(' expr ')' 
            | '[' matrixinitializer ']'
            | expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr MPLUS expr
            | expr MMINUS expr
            | expr MTIMES expr
            | expr MDIVIDE expr
            | expr EQ expr
            | expr NEQ expr
            | expr '>' expr
            | expr '<' expr
            | expr LEQ expr
            | expr GEQ expr
            """
    if len(p)==5:
        p[0] = AST.MatWord(p[1], p[3])
    elif len(p) == 4:
        if p[1] == '(' or p[1] == '[' or p[1] == '{':
            p[0] = p[2]
        else:
            p[0] = AST.BinExpr(p[2], p[1], p[3])
    elif len(p) == 3:
        if p[1] == '-':
            p[0] = AST.UnaryMinus(p[2])
        else:
            p[0] = AST.UnaryTranspose(p[1])

def p_special_matrix_word(p):
    """specialmatrixword : ZEROS
                            | ONES
                            | EYE"""
    p[0] = p[1]


def p_if_statement(p):
    """ifstatement : IF '(' expr ')' block %prec IFX
                    | IF '(' expr ')' block ELSE block"""
    if len(p) > 6:
        p[0] = AST.IfElse(p[3], p[5], p[7])
    else:
        p[0] = AST.IfElse(p[3], p[5])

def p_loop(p):
    """loop : forloop
            | whileloop"""
    p[0] = p[1]


def p_for_loop(p):
    """forloop : FOR ID '=' rangeoperator block"""
    p[0] = AST.ForLoop(p[2], p[4], p[5])


def p_while_loop(p):
    """whileloop : WHILE '(' expr ')' block"""
    p[0] = AST.WhileLoop(p[3], p[5])


def p_range_op(p):
    """rangeoperator : expr ':' expr """
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_matrix_initializer(p):
    """matrixinitializer : '[' innerlist  ']'
                        | vector ',' '[' innerlist ']' """
    if len(p) < 5:
        p[0] = AST.Vector(p[2])
    else:
        p[0] = AST.Matrix(p[1], AST.Vector(p[4]))


def p_vector(p):
    """vector : '[' innerlist  ']'
              | vector ',' '[' innerlist  ']'"""
    if len(p) < 5:
        p[0] = AST.Vector(p[2])
    else:
        p[0] = AST.Node(p[1], AST.Vector(p[4]))


def p_innerlist(p):
    """innerlist : expr  
                | innerlist ',' expr"""
    if len(p) < 3:
        p[0] = p[1]
    else:
        p[0] = AST.Node(p[1], p[3])


parser = yacc.yacc()
# Mparser.py
# Wyświetlam Mparser.py.
