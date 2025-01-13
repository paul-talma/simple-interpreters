from dataclasses import dataclass


@dataclass
class TokenTypes:
    LAMBDA = "LAMBDA"
    LPAR = "LPAR"
    RPAR = "RPAR"
    DOT = "DOT"
    VAR = "VAR"
    EOS = "EOS"


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Type: {self.type}, value: {self.value}"

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, input):
        self.input = input
        self.pos = 0
        self.max_len = len(input)
        self.char = input[0]

    def advance(self):
        self.pos += 1
        if self.pos < self.max_len:
            self.char = self.input[self.pos]
        else:
            self.char = None

    def skip_spaces(self):
        while self.char is not None and self.char.isspace():
            self.advance()

    def error(self):
        raise Exception("Lexer error.")

    def get_word(self):
        word = ""
        while self.char is not None and self.char.isalnum():
            word += self.char
            self.advance()
        if word == "lambda":
            return Token(TokenTypes.LAMBDA, "lambda")
        return Token(TokenTypes.VAR, word)

    def get_token(self):
        if self.pos >= self.max_len:
            return Token(TokenTypes.EOS, None)

        if self.char.isspace():
            self.skip_spaces()
            return self.get_token()

        if self.char == "\\":
            self.advance()
            return Token(TokenTypes.LAMBDA, "\\")

        if self.char == "(":
            self.advance()
            return Token(TokenTypes.LPAR, "(")

        if self.char == ")":
            self.advance()
            return Token(TokenTypes.RPAR, ")")

        if self.char == ".":
            self.advance()
            return Token(TokenTypes.DOT, ".")

        if self.char.isalpha():
            token = self.get_word()
            return token
