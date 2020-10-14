import ply.lex as lex

reserved = {'zeros' : 'ZEROS'}

tokens = ['COMMENT', 'MPLUS', 'MMINUS', 'MTIMES', 'MDIVIDE', 'NUMBER',
          'ASSIGNPLUS', 'ASSIGNMINUS', 'ASSIGNTIMES', 'ASSIGNDIVIDE', 'ID'] + list(reserved.values())

t_COMMENT = r'\#.*'
t_MPLUS = r'.\+'
t_MMINUS = r'.-'
t_MTIMES = r'.\*'
t_MDIVIDE = r'./'
t_ASSIGNPLUS = r'\+='
t_ASSIGNMINUS = r'-='
t_ASSIGNTIMES = r'\*='
t_ASSIGNDIVIDE = r'/='



literals = "+-*/()[]{}="




def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')
    return t


t_ignore = '  \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print
    "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()
