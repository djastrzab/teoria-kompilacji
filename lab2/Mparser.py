#!/usr/bin/python

import scanner
import ply.yacc as yacc


tokens = scanner.tokens

symtab = {}

precedence = (
   # to fill ...
    ("right", '=', "ASSIGNPLUS", "ASSIGNMINUS", "ASSIGNTIMES", "ASSIGNDIVIDE"),
    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
    ("nonassoc", '(', ')'),
    ("nonassoc", '<', '>', "EQ", "NEQ", "LEQ", "GEQ"),
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
    # LOL - MORESTATEMENTS STATEMENT jest kluczowe by to wgl moglo dzialac XDDDD (bez tego nie umie to ogarnac wiecej niz 1 instrukcji)
    """MORESTATEMENTS : STATEMENT
                    |  STATEMENT MORESTATEMENTS
                    | '{' MORESTATEMENTS '}'"""

def p_statement(p):
    """STATEMENT : IFSTATEMENT
                | LOOP
                | EXPR ';'
                | RETURNSTATEMENT ';'
                | ASSIGNSTATEMENT ';'
                | PRINTSTATEMENT ';'
                | BREAK ';'
                | CONTINUE ';'""" # Dwa ostatnie na pewno nie powinny tu byc, bo CONTINUE i BREAK powinny sie pojawiac tylko w petlach

def p_return_statement(p):
    """RETURNSTATEMENT : RETURN
                        | RETURN EXPR"""

def p_print_statement(p):
    """PRINTSTATEMENT : PRINT PRINTABLE"""

def p_pritable(p):
    """PRINTABLE : PRINTABLE ',' PRINTABLE
                | ARITHMETICOPERATION
                | LOGICALEXPR
                | STRING"""

def p_assign_statement(p):
    """ASSIGNSTATEMENT : ID '=' EXPR
                        | ID ASSIGNPLUS EXPR
                        | ID ASSIGNMINUS EXPR
                        | ID ASSIGNTIMES EXPR
                        | ID ASSIGNDIVIDE EXPR"""

def p_expr(p):
    """EXPR : ARITHMETICOPERATION
            | MATRIXOPERATION
            | LOGICALEXPR"""


def p_logical_expr(p):
    """LOGICALEXPR : ARITHMETICOPERATION EQ ARITHMETICOPERATION
                    | ARITHMETICOPERATION NEQ ARITHMETICOPERATION
                    | ARITHMETICOPERATION '>' ARITHMETICOPERATION
                    | ARITHMETICOPERATION '<' ARITHMETICOPERATION
                    | ARITHMETICOPERATION LEQ ARITHMETICOPERATION
                    | ARITHMETICOPERATION GEQ ARITHMETICOPERATION"""

def p_arithmetic_op(p):
    """ARITHMETICOPERATION : ID
                        | INTNUMBER
                        | FLOATNUMBER
                        | '(' ARITHMETICOPERATION ')' 
                        | ARITHMETICOPERATION '+' ARITHMETICOPERATION
                        | ARITHMETICOPERATION '-' ARITHMETICOPERATION
                        | ARITHMETICOPERATION '*' ARITHMETICOPERATION
                        | ARITHMETICOPERATION '/' ARITHMETICOPERATION
                        | '-' ARITHMETICOPERATION"""

def p_matrix_op(p):
    """MATRIXOPERATION : ID
                        | '(' MATRIXOPERATION ')'
                        | MATRIXOPERATION "\'"
                        | MATRIXOPERATION MPLUS MATRIXOPERATION
                        | MATRIXOPERATION MMINUS MATRIXOPERATION
                        | MATRIXOPERATION MTIMES MATRIXOPERATION
                        | MATRIXOPERATION MDIVIDE MATRIXOPERATION
                        | SPECIALMATRIXWORD '(' ARITHMETICOPERATION ')'"""

def p_special_matrix_word(p):
    """SPECIALMATRIXWORD : ZEROS
                            | ONES
                            | EYE"""

def p_if_statement(p):
    """IFSTATEMENT : IF '(' LOGICALEXPR ')' MORESTATEMENTS %prec IFX
                    | IF '(' LOGICALEXPR ')' MORESTATEMENTS ELSE MORESTATEMENTS"""

def p_loop(p):
    """LOOP : FORLOOP
            | WHILELOOP"""

def p_for_loop(p):
    """FORLOOP : FOR ID '=' RANGEOPERATOR MORESTATEMENTS"""

def p_while_loop(p):
    """WHILELOOP : WHILE '(' LOGICALEXPR ')' MORESTATEMENTS"""

def p_range_op(p):
    """RANGEOPERATOR : ARITHMETICOPERATION ':' ARITHMETICOPERATION """

# Na pewno trzeba cos z listami/macierzami jeszcze zrobic bo zapis [1, 2, 3] nie jest wgl czytany





parser = yacc.yacc()
