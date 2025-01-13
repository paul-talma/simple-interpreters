from terms import Term
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from transpiler import LatexTranspiler


def parse(text: str) -> Term:
    """
    args:
    text: raw input string

    returns:
    an AST representing the corresponding lambda expression
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    return tree


def interpret(input_tree: Term) -> Term:
    """
    args:
    input_tree: an AST object representing a lambda expression

    returns:
    an AST object representing the normal form of the lambda expression
    """
    interpreter = Interpreter(input_tree)
    output_tree = interpreter.interpret()
    return output_tree


def transpile(tree: Term) -> str:
    """
    args:
    input_tree: an AST object representing a lambda expression

    returns:
    a latex string for rendering the corresponding lambda expression
    """
    transpiler = LatexTranspiler(tree)
    latex_formula = transpiler.transpile()
    return latex_formula
