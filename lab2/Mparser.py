
#!/usr/bin/python

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

def p_more_statements(p):
    """morestatements : statement
                    |  statement morestatements
                    | '{' morestatements '}'"""

def p_statement(p):
    """statement : ifstatement
                | loop
                | expr ';'
                | returnstatement ';'
                | assignstatement ';'
                | printstatement ';'
                | BREAK ';'
                | CONTINUE ';'"""

def p_return_statement(p):
    """returnstatement : RETURN 
                        | RETURN expr"""

def p_print_statement(p):
    """printstatement : PRINT printables"""

def p_printables(p):
    """printables : printable
                | printables ',' printable"""

def p_pritable(p):
    """printable : expr
                | STRING"""

def p_assign_statement(p):
    """assignstatement : assignable '=' expr
                        | assignable ASSIGNPLUS expr
                        | assignable ASSIGNMINUS expr
                        | assignable ASSIGNTIMES expr
                        | assignable ASSIGNDIVIDE expr"""

def p_assignable(p):
    """assignable : ID
                    | matrixaccess"""

def p_matrix_access(p):
    """matrixaccess : ID '[' expr ',' expr ']'"""

def p_expr(p):
    """expr : assignable
            | INTNUMBER
            | FLOATNUMBER
            | '[' matrixinitializer ']'
            | specialmatrixword '(' expr ')'
            | '-' expr %prec UNARY
            | expr "\'"
            | '(' expr ')' 
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

def p_special_matrix_word(p):
    """specialmatrixword : ZEROS
                            | ONES
                            | EYE"""

def p_if_statement(p):
    """ifstatement : IF '(' expr ')' morestatements %prec IFX
                    | IF '(' expr ')' morestatements ELSE morestatements"""

def p_loop(p):
    """loop : forloop
            | whileloop"""

def p_for_loop(p):
    """forloop : FOR ID '=' rangeoperator morestatements"""

def p_while_loop(p):
    """whileloop : WHILE '(' expr ')' morestatements"""

def p_range_op(p):
    """rangeoperator : expr ':' expr """

def p_matrix_initializer(p):
    """matrixinitializer : '[' innerlist  ']'
                        | matrixinitializer ',' '[' innerlist ']' """

def p_innerlist(p):
    """innerlist : expr  
                | innerlist ',' expr"""

parser = yacc.yacc()
#Mparser.py
#Wyświetlam Mparser.py.