# class for tokens
# class for interpreter
# main method taking input and interpreting it

# token class just stores the type and value of the token
# interpreter class initialized with input, implements lexer,
# and implements evaluation of input

INTEGER, PLUS, MINUS, TIMES, DIV, EOS = "INTEGER", "PLUS", "MINUS", "TIMES", "DIV", "EOS"


class Token:
    """
    Stores a token as a (type, value) pair.
    """

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()


class Interpreter:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.max_len = len(text)
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Unable to parse input.")

    def advance(self):
        self.pos += 1
        if self.pos < self.max_len:
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
        

    def get_next_token(self):
        if self.pos >= self.max_len:
            return Token(EOS, None)

        if self.current_char.isspace():
            self.skip_space()
            return self.get_next_token()
        if self.current_char.isdigit():
            return Token(INTEGER, self.get_int())
        if self.current_char == "+":
            self.advance()
            return Token(PLUS, "+")
        if self.current_char == "-":
            self.advance()
            return Token(MINUS, "-")
        if self.current_char == "*":
            self.advance()
            return Token(TIMES, "*")
        if self.current_char == "/":
            self.advance()
            return Token(DIV, "/")
        self.error()

    def skip_space(self):
        while self.current_char.isspace():
            self.advance()

    def get_int(self):
        int_str = ""
        while self.current_char is not None and self.current_char.isdigit():
            int_str += self.current_char
            self.advance()
        return int(int_str)

    def eat(self, type):
        """
        Intuitively: call eat(TYPE) when finished processing some token of type TYPE
        This loads the next token in self.current_token
        """
        if self.current_token.type == type:
            self.current_token = self.get_next_token()
        else:
            raise self.error()

    def term(self):
        val = self.current_token.value
        self.eat(INTEGER)
        return val

    def eval(self):
        self.current_token = self.get_next_token()

        res = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                res += self.term()
            if token.type == MINUS:
                self.eat(MINUS)
                res -= self.term()
        
        return res

        

def main():
    while True:
        try:
            text = input("calc>")
        except EOFError:
            print("Invalid input")
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.eval()
        print(result)


if __name__ == "__main__":
    main()
