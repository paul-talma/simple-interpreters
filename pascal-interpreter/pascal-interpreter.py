# grammar:
	# program : compound_statement DOT
	# compound_statement : BEGIN statement_list END
	# statement_list : statement | statement SEMI statement_list
	# statement : compound_statement | assignment_statement | empty
	# assignment_statement : variable ASSIGN expr
	# empty :
	# expr : term ((PLUS|MINUS) term)*
	# term : factor ((MUL|DIV) factor)*
	# factor : (PLUS|MINUS)factor | INTEGER | LP expr RP | variable
	# variable: ID

# tokens
INT = "INT"
PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
DIV = "DIV"
LP = "LP"
RP = "RP"
BEGIN = "BEGIN"
END = "END"
DOT = "DOT"
ID = "ID"
ASSIGN = "ASSIGN"
SEMI = "SEMI"
EOS = "EOS"

#############################################
#					Tokens					#
#############################################

class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __str__(self):
		"""String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
		return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

	def __repr__(self):
		return self.__str__()
	

RESERVED_KEYWORDS = {
	'BEGIN': Token(BEGIN, 'BEGIN'),
	'END': Token(END, 'END')
}

#############################################
#					Lexer					#
#############################################

class Lexer:
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.max_len = len(text)
		self.ch = text[0]

	def advance(self):
		self.pos += 1
		if self.pos < self.max_len:
			self.ch = self.text[self.pos]
		else:
			self.ch = None

	def skip_spaces(self):
		while self.ch is not None and self.ch.isspace():
			self.advance()

	def get_int(self):
		num = ""
		while self.ch is not None and self.ch.isdigit():
			num += self.ch
			self.advance()
		return Token(INT, int(num))

	def peek(self):
		if self.pos + 1 < self.max_len:
			return self.text[self.pos + 1]
		else:
			return None

	def error(self):
		raise Exception("Lexer error.")

	def _id(self):
		id = ""
		while self.ch is not None and self.ch.isalnum():
			id += self.ch
			self.advance()

		token = RESERVED_KEYWORDS.get(id, Token(ID, id))
		return token

	def get_token(self):
		if self.pos >= self.max_len:
			return Token(EOS, None)

		if self.ch.isspace():
			self.skip_spaces()
			return self.get_token()

		if self.ch.isdigit():
			return self.get_int()

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

		if self.ch == '.':
			self.advance()
			return Token(DOT, '.')

		if self.ch == ';':
			self.advance()
			return Token(SEMI, ';')

		if self.ch == ':' and self.peek() == '=':
			self.advance()
			self.advance()
			return Token(ASSIGN, ':=')

		if self.ch.isalpha():
			return self._id()

class AST:
	pass

#############################################
#				AST Node Types				#
#############################################

class Compound(AST):
	def __init__(self, statement_list):
		self.statement_list = statement_list

class Assignment(AST):
	def __init__(self, var, op, expr):
		self.var = var
		self.op = op 					# why is this needed?
		self.expr = expr

class UnOp(AST):
	def __init__(self, op, expr):
		self.op = op.type
		self.expr = expr

class BinOp(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

class Num(AST):
	def __init__(self, value):
		self.value = value

class Variable(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value

class Empty(AST):
	pass

#############################################
#					Parser					#
#############################################

class Parser:
	def __init__(self, lexer):
		self.lexer = lexer
		self.token = lexer.get_token()

	def error(self):
		raise Exception("Parser error.")

	def eat(self, type):
		if self.token.type == type:
			self.token = self.lexer.get_token()
		else:
			self.error()

	def program(self):
		tree = self.compound_statement()
		self.eat(DOT)
		return tree

	def compound_statement(self):
		self.eat(BEGIN)
		statements = self.statement_list()
		root = Compound(statements)
		self.eat(END)
		return root

	def statement_list(self):
		statements = [self.statement()]
		while self.token.type == SEMI:
			self.eat(SEMI)
			statements.append(self.statement())
		return statements

	def assigment_statement(self):
		var = self.variable()
		op = self.token
		self.eat(ASSIGN)
		expr = self.expr()
		return Assignment(var, op, expr)

	def statement(self):
		if self.token.type == ID:
			return self.assigment_statement()
		elif self.token.type == BEGIN:
			return self.compound_statement()
		else:
			return self.empty()

	def empty(self):
		return Empty()

	def variable(self):
		var = self.token
		self.eat(ID)
		return Variable(var)

	def factor(self):
		token = self.token
		if token.type == INT:
			num = Num(token.value)
			self.eat(INT)
			return num
		if token.type == LP:
			self.eat(LP)
			expr = self.expr()
			self.eat(RP)
			return expr
		if token.type == PLUS or token.type == MINUS:
			self.eat(token.type)
			return UnOp(token, self.factor())
		if token.type == ID:
			return self.variable()

	def term(self):
		node = self.factor()
		while self.token.type == MUL or self.token.type == DIV:
			op = self.token
			self.eat(op.type)
			right_term = self.factor()
			node = BinOp(node, op, right_term)
		return node

	def expr(self):
		node = self.term()
		while self.token.type == PLUS or self.token.type == MINUS:
			op = self.token
			self.eat(op.type)
			right_term = self.term()
			node = BinOp(node, op, right_term)
		return node

	def parse(self):
		tree = self.program()
		if self.token.type != EOS:
			self.error()
		return tree


#############################################
#				  Interpreter				#
#############################################

class NodeVisitor:
	def visit(self, node):
		name = "visit_" + type(node).__name__
		visitor = getattr(self, name, self.default_visitor)
		return visitor(node)

	def default_visitor(self, node):
		raise Exception(f"No method named visit_{type(node).__name__}.")

class Interpreter(NodeVisitor):
	GLOBAL_SCOPE = {}

	def __init__(self, parser):
		self.parser = parser

	def interpret(self):
		tree = self.parser.parse()
		if tree is None:
			return ''
		return self.visit(tree)

	def visit_Num(self, num_node):
		return num_node.value

	def visit_Variable(self, var_node):
		var_name = var_node.value
		val = self.GLOBAL_SCOPE.get(var_name)
		if val == None:
			raise NameError(repr(var_name))
		else:
			return val

	def visit_UnOp(self, un_op):
		if un_op.op == PLUS:
			return self.visit(un_op.expr)
		if un_op.op == MINUS:
			return -self.visit(un_op.expr)

	def visit_BinOp(self, bin_op):
		left = bin_op.left
		op = bin_op.op.type
		right = bin_op.right
		if op == PLUS:
			return self.visit(left) + self.visit(right)
		if op == MINUS:
			return self.visit(left) - self.visit(right)
		if op == MUL:
			return self.visit(left) * self.visit(right)
		if op == DIV:
			return self.visit(left) // self.visit(right)

	def visit_Compound(self, compound):
		for statement in compound.statement_list:
			self.visit(statement)

	def visit_Assignment(self, assignment):
		var_name = assignment.var.value
		self.GLOBAL_SCOPE[var_name] = self.visit(assignment.expr)

	def visit_Empty(self, node):
		pass

def main():
	import sys

	print("="*41)
	print("Welcome to your Simple Pascal Interpreter")
	print("="*41)
	# while True:
	# text = open(sys.argv[1], 'r').read()
	# filename = filename.strip()
	# with open(filename, 'r') as fid:
	# 	text = ""
	# 	for line in fid.readlines():
	# 		text += line.strip() + " "

	text = open("/Users/paultalma/Programming/simple-interpreters/pascal-interpreter/test.txt", 'r').read()
	lexer = Lexer(text)
	parser = Parser(lexer)
	interpreter = Interpreter(parser)
	result = interpreter.interpret()
	print(interpreter.GLOBAL_SCOPE)

if __name__ == "__main__":
	main()
