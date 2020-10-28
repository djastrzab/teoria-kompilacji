#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
   # to fill ...
   ("left", '+', '-'),
   # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_binary_operators(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | INTNUMBER"""
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

def p_term_assign(p):
    """term : ID '=' reserved"""
    p[0] = p[2]



# to finish the grammar
# ....





parser = yacc.yacc()
