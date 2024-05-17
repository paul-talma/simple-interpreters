
INTEGER, PLUS, MINUS, TIMES, DIV, LPAR, RPAR, EOS = "INTEGER", "PLUS", "MINUS", "TIMES", "DIV", "LPAR", "RPAR", "EOS"


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


class Lexer:
	"""
	Tokenizes input.
	Call `get_next_token` to get next token in input
	"""
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.max_len = len(text)
		self.current_char = self.text[self.pos]

	def error(self):
		raise Exception("Invalid character.")

	def advance(self):
		self.pos += 1
		if self.pos < self.max_len:
			self.current_char = self.text[self.pos]
		else:
			self.current_char = None

	def skip_space(self):
		while self.current_char.isspace():
			self.advance()

	def get_int(self):
		int_str = ""
		while self.current_char is not None and self.current_char.isdigit():
			int_str += self.current_char
			self.advance()
		return int(int_str)

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
		
		if self.current_char == "(":
			self.advance()
			return Token(LPAR, "(")
		
		if self.current_char == ")":
			self.advance()
			return Token(RPAR, ")")

		self.error()

class Interpreter:
	"""
	Contains a parser and interpreter.
	Parser structures stream of tokens produced by lexer.
	Interpreter computes the structure given by the parser
	"""
	def __init__(self, lexer):
		self.lexer = lexer
		self.pos = 0
		self.current_token = self.lexer.get_next_token()

	def error(self):
		raise Exception("Invalid syntax.")

	def eat(self, type):
		if self.current_token.type == type:
			self.current_token = self.lexer.get_next_token()
		else:
			raise self.error()

	def factor(self):
		"""
		factor : INTEGER | LPAR expr RPAR
		"""
		if self.current_token.type == INTEGER:
			result = self.current_token.value
			self.eat(INTEGER)
		elif self.current_token.type == LPAR:
			self.eat(LPAR)
			result = self.expr()
			self.eat(RPAR)
		
		return result

	def term(self):
		"""
		term : factor((TIMES | DIV) factor)*
		"""
		result = self.factor()

		while self.current_token.type in (TIMES, DIV):
			token = self.current_token
			if token.type == TIMES:
				self.eat(TIMES)
				result *= self.factor()
			if token.type == DIV:
				self.eat(DIV)
				div = self.factor()
				if div == 0:
					raise ZeroDivisionError("Dividing by 0!")
				result /= self.factor()
		return result

	def expr(self):
		"""
		expr : term((PLUS | MINUS) term)*
		"""
		result = self.term()

		while self.current_token.type in (PLUS, MINUS):

			token = self.current_token
			if token.type == PLUS:
				self.eat(PLUS)
				result += self.term()
			if token.type == MINUS:
				self.eat(MINUS)
				result -= self.term()

		return result



def main():
    while True:
        try:
            text = input("calc>")
        except EOFError:
            print("Invalid input")
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
