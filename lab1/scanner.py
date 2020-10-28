import ply.lex as lex

reserved = {'zeros': 'ZEROS',
            'eye': 'EYE',
            'ones': 'ONES',
            'break': 'BREAK',
            'continue': 'CONTINUE',
            'return': 'RETURN',
            'print': 'PRINT',
            'if': 'IF',
            'else': 'ELSE',
            'for': 'FOR',
            'while': 'WHILE'}

tokens = ['MPLUS', 'MMINUS', 'MTIMES', 'MDIVIDE', 'INTNUMBER',
          'ASSIGNPLUS', 'ASSIGNMINUS', 'ASSIGNTIMES', 'ASSIGNDIVIDE',
          'LEQ', 'EQ', 'GEQ', 'NEQ', 'FLOATNUMBER', 'STRING', 'ID'] + list(reserved.values())

t_MPLUS = r'\.\+'
t_MMINUS = r'\.-'
t_MTIMES = r'\.\*'
t_MDIVIDE = r'\./'
t_ASSIGNPLUS = r'\+='
t_ASSIGNMINUS = r'-='
t_ASSIGNTIMES = r'\*='
t_ASSIGNDIVIDE = r'/='
t_LEQ = r'<='
t_EQ = r'=='
t_GEQ = r'>='
t_NEQ = r'!='

literals = "+-*/()[]{}=<>,;:'"


def t_FLOATNUMBER(t):
    r'(\.\d+|\d+\.\d*)((E|e)(\+|-)?\d+)?'
    t.value = float(t.value)
    return t


def t_INTNUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'".*?"'
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_COMMENT(t):
    r'\#.*'
    pass


t_ignore = '  \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    if(t):
        print("!(%d)!: Illegal token '%s'!" % (t.lexer.lineno, t.value[0]))
    else:
        print("Unexpected end of input!")
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()
