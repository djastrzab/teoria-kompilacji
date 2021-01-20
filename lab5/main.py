import sys
import ply.yacc as yacc
import Mparser
import scanner
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "pi.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = yacc.yacc(module=Mparser)
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)
    # if not Mparser.incorrect_input:
    #     ast.printTree()

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)

    interpreter = Interpreter.Interpreter()
    interpreter.interpret(ast)
    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())
