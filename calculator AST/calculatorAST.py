INT, PLUS, MINUS, MUL, DIV, LPAR, RPAR, EOS = "INT", "PLUS", "MINUS", "MUL", "DIV", "LPAR", "RPAR", "EOS"


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
		while self.current_char is not None and self.current_char.isspace():
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
			return Token(INT, self.get_int())

		if self.current_char == "+":
			self.advance()
			return Token(PLUS, "+")

		if self.current_char == "-":
			self.advance()
			return Token(MINUS, "-")

		if self.current_char == "*":
			self.advance()
			return Token(MUL, "*")

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


class AST():
	pass

class BinOp(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class Num(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value

class Parser:
	def __init__(self, lexer):
		self.current_token = lexer.get_next_token()
		self.lexer = lexer

	def eat(self, type):
		if self.current_token.type == type:
			self.current_token = self.lexer.get_next_token()
		else:
			raise Exception("Unable to parse!")

	def factor(self):
		token = self.current_token
		if token.type == INT:
			self.eat(INT)
			return Num(token)
		elif token.type == LPAR:
			self.eat(LPAR)
			result = self.expr()
			self.eat(RPAR)
			return result


	def term(self):
		node = self.factor()

		while self.current_token.type == MUL or self.current_token.type == DIV:
			token = self.current_token
			if token.type == MUL:
				self.eat(MUL)
				node = BinOp(node, token, self.factor())
			elif token.type == DIV:
				self.eat(DIV)
				node = BinOp(node, token, self.factor())

		return node


	def expr(self):
		node = self.term()

		while self.current_token.type == PLUS or self.current_token.type == MINUS:
			token = self.current_token
			if token.type == PLUS:
				self.eat(PLUS)
				node = BinOp(node, token, self.term())
			elif token.type == MINUS:
				self.eat(MINUS)
				node = BinOp(node, token, self.term())

		return node

	def parse(self):
		return self.expr()

class NodeVisitor: # this is cool
	def visit(self, node):
		method_name = 'visit_' + type(node).__name__
		visitor = getattr(self, method_name, self.generic_visit)
		return visitor(node)

	def generic_visit(self, node):
		raise Exception(f"No visit_{type(node).__name__} method")


class Interpreter(NodeVisitor):
	def __init__(self, parser):
		self.parser = parser

	def visit_BinOp(self, node):
		if node.op.type == PLUS:
			return self.visit(node.left) + self.visit(node.right)
		if node.op.type == MINUS:
			return self.visit(node.left) - self.visit(node.right)
		if node.op.type == MUL:
			return self.visit(node.left) * self.visit(node.right)
		if node.op.type == DIV:
			return self.visit(node.left) // self.visit(node.right)

	def visit_Num(self, node):
		return node.value

	def interpret(self):
		tree = self.parser.parse()
		return self.visit(tree)

def main():
	print("="*41)
	print("Welcome to your Simple Pascal Interpreter")
	print("="*41)
	while True:
		try:
			text = input("SPI>")
		except EOFError:
			print("Invalid input")
			break
		if not text:
			continue
		lexer = Lexer(text)
		parser = Parser(lexer)
		interpreter = Interpreter(parser)
		result = interpreter.interpret()
		print(result)

if __name__ == "__main__":
	main()
