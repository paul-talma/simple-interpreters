# translates string input into LISP notation
# e.g. (1+2)*3 |-> (* (+ 1 2) 3)

INT = "INT"
PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
DIV = "DIV"
LP = "LP"
RP = "RP"
EOS = "EOS"

class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

class Lexer:
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.max_len = len(text)
		self.ch = text[0]

	def get_next_token(self):
		if self.pos >= self.max_len:
			return Token(EOS, None)

		if self.ch.isspace():
			self.skip_space()
			return self.get_next_token()

		if self.ch.isdigit():
			return Token(INT, self.get_int())

		if self.ch == '+':
			self.advance()
			return Token(PLUS, '+')

		if self.ch == '-':
			self.advance()
			return Token(MINUS, '-')

		if self.ch == '*':
			self.advance()
			return Token(MUL, '*')

		if self.ch == '/':
			self.advance()
			return Token(DIV, '/')

		if self.ch == '(':
			self.advance()
			return Token(LP, '(')

		if self.ch == ')':
			self.advance()
			return Token(RP, ')')

		raise Exception("Lexer error.")

	def advance(self):
		self.pos += 1
		if self.pos >= self.max_len:
			self.ch = None
		else:
			self.ch = self.text[self.pos]

	def skip_space(self):
		while self.ch is not None and self.ch.isspace():
			self.advance()

	def get_int(self):
		num = ""
		while self.ch is not None and self.ch.isdigit():
			num += self.ch
			self.advance()
		return int(num)

class AST:
	pass

class BinOp(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

class Num(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value

class Parser:
	def __init__(self, lexer):
		self.lexer = lexer
		self.token = lexer.get_next_token()

	def eat(self, type):
		if self.token.type == type:
			self.token = self.lexer.get_next_token()
		else:
			raise Exception("Parser error.")

	def factor(self):
		if self.token.type == INT:
			num = self.token
			self.eat(INT)
			return Num(num)
		if self.token.type == LP:
			self.eat(LP)
			num = self.expr()
			self.eat(RP)
			return num

	def term(self):
		node = self.factor()

		while self.token.type == MUL or self.token.type == DIV:
			op = self.token

			if op.type == MUL:
				self.eat(MUL)
			if op.type == DIV:
				self.eat(DIV)

			node = BinOp(node, op, self.factor())

		return node

	def expr(self):
		node = self.term()

		while self.token.type == PLUS or self.token.type == MINUS:
			op = self.token

			if op.type == PLUS:
				self.eat(PLUS)
			if op.type == MINUS:
				self.eat(MINUS)

			node = BinOp(node, op, self.factor())

		return node

	def parse(self):
		return self.expr()

class NodeVisitor:
	def visit(self, node):
		name = "visit_" + type(node).__name__
		visitor = getattr(self, name, self.generic_visit)
		return visitor(node)

	def generic_visit(self, node):
		raise Exception(f"No visit_{type(node).__name__} method")

class Translator(NodeVisitor):
	def __init__(self, parser):
		self.parser = parser

	def visit_BinOp(self, node):
		left = self.visit(node.left)
		right = self.visit(node.right)
		return "(" + node.op.value + " " + left + " " + right + ")"

	def visit_Num(self, node):
		return str(node.value)

	def translate(self):
		tree = self.parser.parse()
		return self.visit(tree)

def main():
	print("Enter an expression, see it in LISP style!")
	print("="*50)
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
		translator = Translator(parser)
		output = translator.translate()
		print(output)

if __name__ == "__main__":
	main()
