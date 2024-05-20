# grammar:
	# program : PROGRAM variable SEMI block DOT
	# block : declarations compound_statement
	# declarations : VAR (variable_declaration SEMI)+ | empty
	# variable_declaration : ID ((COMMA ID)* COLON type_spec)
	# type_spec : INTEGER | REAL
	# compound_statement : BEGIN statement_list END
	# statement_list : statement | statement SEMI statement_list
	# statement : compound_statement | assignment_statement | empty
	# assignment_statement : variable ASSIGN expr
	# empty :
	# expr : term ((PLUS | MINUS) term)*
	# term : factor ((MUL | INT_DIV | FLOAT_DIV) factor)*
	# factor : (PLUS | MINUS)factor | INT_CONST | FLOAT_CONST | LP expr RP | variable
	# variable: ID



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
		return f"Token({self.type}, {repr(self.value)})"

	def __repr__(self):
		return self.__str__()

# token types
INTEGER = "INTEGER"
FLOAT = "FLOAT"
INT_CONST = "INT_CONST"
FLOAT_CONST = "FLOAT_CONST"
PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
INT_DIV = "INT_DIV"
FLOAT_DIV = "FLOAT_DIV"
LP = "LP"
RP = "RP"
BEGIN = "BEGIN"
END = "END"
COMMA = "COMMA"
COLON = "COLON"
DOT = "DOT"
ID = "ID"
ASSIGN = "ASSIGN"
SEMI = "SEMI"
PROGRAM = "PROGRAM"
VAR = "VAR"
EOS = "EOS"

RESERVED_KEYWORDS = {
	'BEGIN': Token(BEGIN, 'BEGIN'),
	'END': Token(END, 'END'),
	'DIV': Token(INT_DIV, 'DIV'),
	'VAR': Token(VAR, 'VAR'),
	'INTEGER': Token(INTEGER, 'INTEGER'),
	'FLOAT': Token(FLOAT, 'FLOAT'),
	'PROGRAM': Token(PROGRAM, 'PROGRAM')
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

	def get_num(self):
		num = ""
		while self.ch is not None and self.ch.isdigit():
			num += self.ch
			self.advance()

		if self.ch == '.' and self.peek().isdigit():
			num += self.ch
			self.advance()
			while self.ch is not None and self.ch.isdigit():
				num += self.ch
				self.advance()
			return Token(FLOAT_CONST, float(num))
		
		return Token(INT_CONST, int(num))

	def peek(self):
		if self.pos + 1 < self.max_len:
			return self.text[self.pos + 1]
		else:
			return None

	def error(self):
		raise Exception("Lexer error.")

	def skip_comment(self):
		stack = ['{']
		while stack:
			self.advance()
			if self.ch is not None and self.ch == '{':
				stack.append(self.ch)
			if self.ch is not None and self.ch == '}':
				stack.pop()
			if self.ch is None:
				raise Exception("Unclosed comment.")
		self.advance()

	def _id(self):
		id = ""
		if self.ch == '_':
			if self.peek() is not None and not self.peek().isalnum():
				self.error()
			id += self.ch
			self.advance()
		while self.ch is not None and self.ch.isalnum():
			id += self.ch.upper()
			self.advance()

		token = RESERVED_KEYWORDS.get(id, Token(ID, id.lower()))
		return token

	def get_token(self):
		if self.pos >= self.max_len:
			return Token(EOS, None)

		if self.ch.isspace():
			self.skip_spaces()
			return self.get_token()

		if self.ch.isdigit():
			return self.get_num()

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
			return Token(FLOAT_DIV, '/')

		if self.ch == '(':
			self.advance()
			return Token(LP, '(')

		if self.ch == ')':
			self.advance()
			return Token(RP, ')')

		if self.ch == ',':
			self.advance()
			return Token(COMMA, ',')

		if self.ch == '.':
			self.advance()
			return Token(DOT, '.')

		if self.ch == ':' and self.peek() == '=':
			self.advance()
			self.advance()
			return Token(ASSIGN, ':=')

		if self.ch == ':':
			self.advance()
			return Token(COLON, ':')

		if self.ch == ';':
			self.advance()
			return Token(SEMI, ';')

		if self.ch.isalpha() or self.ch == '_':
			return self._id()

		if self.ch == '{': # supports nexsted comments
			self.skip_comment()
			return self.get_token()


#############################################
#				AST Node Types				#
#############################################
class AST:
	pass

class Program(AST):
	def __init__(self, name, block):
		self.name = name
		self.block = block

class Block(AST):
	def __init__(self, declarations, compound_statement):
		self.declarations = declarations
		self.compound_statement = compound_statement

class Declaration(AST):
	def __init__(self, var_node, type_node):
		self.var_node = var_node
		self.type_node = type_node

	def __str__(self):
		return f"Variable (token: {self.var_node}, type: {self.type_node})"

	def __repr__(self):
		return self.__str__()

class Type(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value
	
	def __str__(self):
		return f"Variable (token: {self.token}, value: {self.value})"

	def __repr__(self):
		return self.__str__()

class Compound(AST):
	def __init__(self, statement_list):
		self.statement_list = statement_list

class Assignment(AST):
	def __init__(self, var, op, expr):
		self.var = var
		self.op = op 					# why is this needed?
		self.expr = expr
	
	def __str__(self):
		return f"Assignment(var: {self.var}, op: {self.op}, expr: {self.expr})"

	def __repr__(self):
		return self.__str__()

class UnOp(AST):
	def __init__(self, op, expr):
		self.op = op.type
		self.expr = expr

	def __str__(self):
		return f"Variable (op: {self.op}, expr: {self.expr})"

	def __repr__(self):
		return self.__str__()

class BinOp(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def __str__(self):
		return f"BinOp (left: {self.left}, op: {self.op}, right: {self.right})"

	def __repr__(self):
		return self.__str__()
class Num(AST):
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return f"Num (value: {self.value})"

	def __repr__(self):
		return self.__str__()

class Variable(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value
	
	def __str__(self):
		return f"Variable (token: {self.token}, name: {self.value})"

	def __repr__(self):
		return self.__str__()

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
		raise Exception(f"Parser error. Token: {self.token}")

	def eat(self, type):
		if self.token.type == type:
			self.token = self.lexer.get_token()
		else:
			self.error()

	def flatten(self, ls):
		return [x for xs in ls for x in xs]

	def program(self):
		self.eat(PROGRAM)
		var = self.variable()
		program_name = var.value
		self.eat(SEMI)
		block = self.block()
		program = Program(program_name, block)

		self.eat(DOT)
		return program

	def block(self):
		declarations = self.declarations()
		statement = self.compound_statement()
		return Block(declarations, statement)

	def declarations(self):
		declarations = []
		if self.token.type == VAR:
			self.eat(VAR)
			declarations = [self.variable_declaration()]
			self.eat(SEMI)
			while self.token.type == ID:
				declarations.append(self.variable_declaration())
				self.eat(SEMI)
			declarations = self.flatten(declarations)
		return declarations

	def variable_declaration(self):
		variables = [Variable(self.token)]
		self.eat(ID)
		while self.token.type == COMMA:
			self.eat(COMMA)
			variables.append(Variable(self.token))
			self.eat(ID)
		self.eat(COLON)
		type = self.type_spec()
		return [Declaration(variable, type) for variable in variables]

	def type_spec(self):
		token = self.token
		if token.type == INTEGER:
			self.eat(INTEGER)
			return Type(token)
		if token.type == FLOAT:
			self.eat(FLOAT)
			return Type(token)

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

	def statement(self):
		if self.token.type == ID:
			return self.assigment_statement()
		elif self.token.type == BEGIN:
			return self.compound_statement()
		else:
			return self.empty()
		
	def assigment_statement(self):
		var = self.variable()
		op = self.token
		self.eat(ASSIGN)
		expr = self.expr()
		return Assignment(var, op, expr)

	def empty(self):
		return Empty()

	def variable(self):
		var = self.token
		self.eat(ID)
		return Variable(var)

	def factor(self):
		token = self.token
		if token.type in (INT_CONST, FLOAT_CONST):
			num = Num(token.value)
			self.eat(token.type)
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
		while self.token.type in (MUL, INT_DIV, FLOAT_DIV):
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
		program = self.parser.parse()
		if program is None:
			return ''
		return self.visit(program)

	def visit_Program(self, program):
		return self.visit(program.block)

	def visit_Block(self, block):
		for declaration in block.declarations:
				self.visit(declaration)

		return self.visit(block.compound_statement)

	def visit_Declaration(self, declaration):
		# var_name = declaration.var_node.value
		# type = self.visit(declaration.type_node)
		# self.GLOBAL_SCOPE[var_name]['type'] = type
		pass

	def visit_Type(self, type_node):
		# return type_node.value
		pass

	def visit_Compound(self, compound):
		for statement in compound.statement_list:
			self.visit(statement)

	def visit_Assignment(self, assignment):
		var_name = assignment.var.value
		self.GLOBAL_SCOPE[var_name] = self.visit(assignment.expr)

	def visit_Variable(self, var_node):
		var_name = var_node.value
		val = self.GLOBAL_SCOPE.get(var_name)
		if val == None:
			raise NameError(repr(var_name))
		else:
			return val

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
		if op == INT_DIV:
			return self.visit(left) // self.visit(right)
		if op == FLOAT_DIV:
			return self.visit(left) / self.visit(right)

	def visit_UnOp(self, un_op):
		if un_op.op == PLUS:
			return self.visit(un_op.expr)
		if un_op.op == MINUS:
			return -self.visit(un_op.expr)

	def visit_Num(self, num_node):
		return num_node.value

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
