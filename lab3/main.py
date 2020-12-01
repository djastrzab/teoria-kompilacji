import sys
import ply.yacc as yacc
import Mparser
import scanner
from TreePrinter import TreePrinter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example3.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = yacc.yacc(module=Mparser)
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)
    if not Mparser.incorrect_input:
        ast.printTree()
