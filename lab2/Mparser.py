#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

symtab = {}

precedence = (
   # to fill ...
    ("right", '=', "ASSIGNPLUS", "ASSIGNMINUS", "ASSIGNTIMES", "ASSIGNDIVIDE"),
    ("left", '+', '-'),
    ("left", '*', '/'),
   # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

def p_start(p):
    # LOL - STATEMENT STATEMENT jest kluczowe by to wgl moglo dzialac XDDDD (bez tego nie umie to ogarnac wiecej niz 1 instrukcji)
    """STATEMENT : STATEMENT STATEMENT      
                | ID ASSIGNSTATMENT ';'
                | EXPR ';'
                | '{' STATEMENT '}'
                | LOOPEXPR
                | IFEXPR
                | RETURN EXPR ';'"""
    if len(p) == 4:     
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = p[1]
    elif p[1] == 'RETURN':  p[0] = p[2]     # return EXP;
    elif p[1] == '{' and p[3] == '}':   p[0] = p[2]
    else:               p[0] = p[1]

def p_assignstatement(p):
    """ASSIGNSTATMENT : '=' EXPR
                    | ASSIGNPLUS ARITHMETICEXPR
                    | ASSIGNMINUS ARITHMETICEXPR
                    | ASSIGNTIMES ARITHMETICEXPR
                    | ASSIGNDIVIDE ARITHMETICEXPR"""
    if p[1] == 'ASSIGNPLUS':    p[0] = p[2]
    elif p[1] == 'ASSIGNMINUS':  p[0] = p[2]
    elif p[1] == 'ASSIGNTIMES':  p[0] = p[2]
    elif p[1] == 'ASSIGNDIVIDE':  p[0] = p[2]

def p_expr(p):
    """EXPR : ARITHMETICEXPR
            | MATRIXEXPR"""
    p[0] = p[1]

def p_arithmeticexpr(p):
    """ARITHMETICEXPR : ID
                    | ARITHMETICEXPR '+' ARITHMETICEXPR
                    | ARITHMETICEXPR '-' ARITHMETICEXPR
                    | ARITHMETICEXPR '*' ARITHMETICEXPR
                    | ARITHMETICEXPR '/' ARITHMETICEXPR
                    | INTNUMBER
                    | FLOATNUMBER"""
    if len(p) > 2:
        if p[2] == '+':     pass#p[0] = p[1] + p[3]
        elif p[2] == '-':   pass#p[0] = p[1] - p[3]
        elif p[2] == '*':   pass#p[0] = p[1] * p[3]
        elif p[2] == '/':   pass#p[0] = p[1] / p[3]

def p_loopexpr(p):
    """LOOPEXPR : ID"""
    pass

def p_ifexpr(p):
    """IFEXPR : ID"""
    pass

def p_matrixexpr(p):
    """MATRIXEXPR : ID"""
    pass


# to finish the grammar
# ....





parser = yacc.yacc()
