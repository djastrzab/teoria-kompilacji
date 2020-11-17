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
    ("nonassoc", '<', '>', "EQ", "NEQ", "LEQ", "GEQ"),
    ("nonassoc", '(', ')'),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", "UNARYR"),
    ("right", "UNARY"),
    
   # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

def p_start(p):
    """MORESTATEMENTS : STATEMENT
                    |  STATEMENT MORESTATEMENTS
                    | '{' MORESTATEMENTS '}'"""

def p_statement(p):
    """STATEMENT : IFSTATEMENT
                | LOOP
                | EXPR ';'
                | RETURNSTATEMENT ';'
                | ASSIGNSTATEMENT ';'
                | PRINTSTATEMENT ';'"""

def p_return_statement(p):
    """RETURNSTATEMENT : RETURN 
                        | RETURN EXPR"""

def p_print_statement(p):
    """PRINTSTATEMENT : PRINT PRINTABLES"""

def p_printables(p):
    """PRINTABLES : PRINTABLE
                | PRINTABLES ',' PRINTABLE"""

def p_pritable(p):
    """PRINTABLE : ARITHMETICOPERATION
                | LOGICALEXPR
                | STRING"""

def p_assign_statement(p):
    """ASSIGNSTATEMENT : ASSIGNABLE '=' EXPR
                        | ASSIGNABLE ASSIGNPLUS EXPR
                        | ASSIGNABLE ASSIGNMINUS EXPR
                        | ASSIGNABLE ASSIGNTIMES EXPR
                        | ASSIGNABLE ASSIGNDIVIDE EXPR"""

def p_assignable(p):
    """ASSIGNABLE : ID
                    | MATRIXACCESS"""

def p_matrix_access(p):
    """MATRIXACCESS : ID '[' ARITHMETICOPERATION ',' ARITHMETICOPERATION ']'"""

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
    """ARITHMETICOPERATION : ASSIGNABLE
                        | INTNUMBER
                        | FLOATNUMBER
                        | '(' ARITHMETICOPERATION ')' 
                        | ARITHMETICOPERATION '+' ARITHMETICOPERATION
                        | ARITHMETICOPERATION '-' ARITHMETICOPERATION
                        | ARITHMETICOPERATION '*' ARITHMETICOPERATION
                        | ARITHMETICOPERATION '/' ARITHMETICOPERATION
                        | '-' ARITHMETICOPERATION %prec UNARY"""

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
    """FORLOOP : FOR ID '=' RANGEOPERATOR LOOPSTATEMENT
                | FOR ID '=' RANGEOPERATOR '{' LOOPSTATEMENTS '}' """

def p_while_loop(p):
    """WHILELOOP : WHILE '(' LOGICALEXPR ')' LOOPSTATEMENT
                | WHILE '(' LOGICALEXPR ')' '{' LOOPSTATEMENTS '}'"""

def p_loop_statements(p):
    """LOOPSTATEMENTS : LOOPSTATEMENT
                        | LOOPSTATEMENT LOOPSTATEMENTS
                        | '{' LOOPSTATEMENTS '}'
                        """

def p_loop_statement(p):
    """LOOPSTATEMENT : IFSTATEMENTWITHLOOPSTATEMENTS
                    | LOOP
                    | EXPR ';'
                    | RETURNSTATEMENT ';'
                    | ASSIGNSTATEMENT ';'
                    | PRINTSTATEMENT ';'
                    | BREAK ';'
                    | CONTINUE ';'"""

def p_matrix_op(p):
    """MATRIXOPERATION : ID
                        | '[' MATRIXINITIALIZER ']'
                        | '(' MATRIXOPERATION ')'
                        | MATRIXOPERATION "\'" %prec UNARYR
                        | MATRIXOPERATION MPLUS MATRIXOPERATION
                        | MATRIXOPERATION MMINUS MATRIXOPERATION
                        | MATRIXOPERATION MTIMES MATRIXOPERATION
                        | MATRIXOPERATION MDIVIDE MATRIXOPERATION
                        | SPECIALMATRIXWORD '(' ARITHMETICOPERATION ')'"""

def p_if_statement_with_loop_statements(p):
    """IFSTATEMENTWITHLOOPSTATEMENTS : IF '(' LOGICALEXPR ')' LOOPSTATEMENTS %prec IFX
                                    | IF '(' LOGICALEXPR ')' LOOPSTATEMENTS ELSE LOOPSTATEMENTS"""

def p_range_op(p):
    """RANGEOPERATOR : ARITHMETICOPERATION ':' ARITHMETICOPERATION """

def p_matrix_initializer(p):
    """MATRIXINITIALIZER : '[' INNERLIST  ']'
                        | MATRIXINITIALIZER ',' '[' INNERLIST ']' """

def p_innerlist(p):
    """INNERLIST : ARITHMETICOPERATION  
                | INNERLIST ',' ARITHMETICOPERATION"""

parser = yacc.yacc()
