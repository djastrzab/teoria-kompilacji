# !/usr/bin/python

import AST
import scanner
import ply.yacc as yacc

tokens = scanner.tokens

symtab = {}

precedence = (
    # to fill ...
    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
    ("nonassoc", '=', "ASSIGNPLUS", "ASSIGNMINUS", "ASSIGNTIMES", "ASSIGNDIVIDE"),
    ("nonassoc", '<', '>', "EQ", "NEQ", "LEQ", "GEQ"),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", "\'"),
    ("right", "UNARY"),
    # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_start(p):
    """start : 
            | morestatements"""
    p[0] = p[1]


def p_more_statements(p):
    """morestatements : statement
                    |  statement morestatements
                    | '{' morestatements '}'"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = AST.Node(p[1], p[2])
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


def p_pritable1(p):         # Fajnie by bylo porozdzielac niektore produkcje na takie podfunkcje
    """printable : expr"""
    p[0] = p[1]

def p_pritable2(p):         # Wtedy nie trzeba kombinowac z niektrorymi if'ami
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
    """expr :  INTNUMBER
            | FLOATNUMBER
            | '-' expr %prec UNARY
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
    else:
        p[0] = AST.IntNum(p[1])     # Chyba sensownie jest porozdzielac to na podfunkcje bo tu nie wychwycimy czy to int czy float
                                    # Alternatywnie mozna zrobic jeden wezel w drzwie na liczby (int i float)

def p_special_matrix_word(p):
    """specialmatrixword : ZEROS
                            | ONES
                            | EYE"""
    p[0] = p[1]


def p_if_statement(p):
    """ifstatement : IF '(' expr ')' morestatements %prec IFX
                    | IF '(' expr ')' morestatements ELSE morestatements"""
    if len(p) > 5:
        p[0] = AST.IfElse(p[3], p[5], p[7])
    else:
        p[0] = AST.IfElse(p[3], p[5])

def p_loop(p):
    """loop : forloop
            | whileloop"""
    p[0] = p[1]


def p_for_loop(p):
    """forloop : FOR ID '=' rangeoperator morestatements"""
    p[0] = AST.ForLoop(p[2], p[4], p[5])


def p_while_loop(p):
    """whileloop : WHILE '(' expr ')' morestatements"""
    p[0] = AST.WhileLoop(p[3], p[5])


def p_range_op(p):
    """rangeoperator : expr ':' expr """
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_matrix_initializer(p):
    """matrixinitializer : '[' innerlist  ']'
                        | matrixinitializer ',' '[' innerlist ']' """


def p_innerlist(p):
    """innerlist : expr  
                | innerlist ',' expr"""


parser = yacc.yacc()
# Mparser.py
# Wyświetlam Mparser.py.
