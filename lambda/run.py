from main.lexer import Lexer
from main.parser import Parser
from main.interpreter import Interpreter
from main.transpiler import LatexTranspiler


def parse(text: str):
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    return tree


def interpret(input_tree):
    interpreter = Interpreter(input_tree)
    output_tree = interpreter.interpret()
    return output_tree


def transpile(tree):
    transpiler = LatexTranspiler(tree)
    latex_formula = transpiler.transpile()
    return latex_formula
