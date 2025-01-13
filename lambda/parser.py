# grammar:
# term: variable | abstraction | application
# abstraction: LAMBDA variable DOT term
# application: LPAR term term RPAR
# variable: VARID


class ParserError(Exception):
    """Unexpected token"""


from main.terms import Variable, Abstraction, Application
from main.lexer import TokenTypes


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.get_token()

    def parse(self):
        tree = self.term()
        if self.token.type != TokenTypes.EOS:
            self.type_error()
        return tree

    def type_error(self, type):
        raise ParserError(
            f"Parser error. Expected type {type} but got Token: {self.token}"
        )

    def eat(self, type):
        if self.token.type == type:
            self.token = self.lexer.get_token()
        else:
            self.type_error(type)

    def term(self):
        if self.token.type == TokenTypes.VAR:
            return self.variable()

        elif self.token.type == TokenTypes.LAMBDA:
            return self.abstraction()

        return self.application()

    # TODO: need to process var.value into a number
    # var.value is a string, e.g. "x2"
    # need to extract the 2
    def variable(self):
        var_token = self.token
        num = self.extract_num(var_token)
        self.eat(TokenTypes.VAR)
        return Variable(num)

    # WARN: this solution is unstable
    # WARN: does not account for different prefixes e.g. x1 vs. y1
    def extract_num(self, var_token):
        val = var_token.value
        return int(val[1:])

    def abstraction(self):
        self.eat(TokenTypes.LAMBDA)
        var = self.variable()
        self.eat(TokenTypes.DOT)
        expr = self.term()
        return Abstraction(var, expr)

    def application(self):
        self.eat(TokenTypes.LPAR)
        expr1 = self.term()
        expr2 = self.term()
        self.eat(TokenTypes.RPAR)
        return Application(expr1, expr2)
