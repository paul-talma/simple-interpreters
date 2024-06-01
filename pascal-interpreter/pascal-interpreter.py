# grammar:
# program : PROGRAM variable SEMI block DOT
# block : declarations compound_statement
# declarations : VAR (variable_declaration SEMI)+
# 			   | (PROCEDURE ID (LP formal_parameter_list RP)? SEMI block SEMI)*
# 			   | empty
# variable_declaration : ID ((COMMA ID)* COLON type_spec)
# type_spec : INTEGER
# 			| REAL
# formal_parameter_list : formal_parameters
# 						| formal_parameters SEMI formal_parameter_list
# formal_parameter : ID (COMMA ID)* COLON type_spec
# compound_statement : BEGIN statement_list END
# statement_list : statement |
# 				 statement SEMI statement_list
# statement : compound_statement
# 			| assignment_statement
# 			| empty
# assignment_statement : variable ASSIGN expr
# empty :
# expr : term ((PLUS | MINUS) term)*
# term : factor ((MUL | INT_DIV | REAL_DIV) factor)*
# factor : (PLUS | MINUS)factor
# 		 | INT_CONST
# 		 | REAL_CONST
# 		 | LP expr RP
# 		 | variable
# variable: ID
from collections import OrderedDict

#############################################
# 					Tokens					#
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
REAL = "REAL"
INT_CONST = "INT_CONST"
REAL_CONST = "REAL_CONST"
PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
INT_DIV = "INT_DIV"
REAL_DIV = "REAL_DIV"
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
PROCEDURE = "PROCEDURE"
EOS = "EOS"

RESERVED_KEYWORDS = {
    "BEGIN": Token(BEGIN, "BEGIN"),
    "END": Token(END, "END"),
    "DIV": Token(INT_DIV, "DIV"),
    "VAR": Token(VAR, "VAR"),
    "INTEGER": Token(INTEGER, "INTEGER"),
    "REAL": Token(REAL, "REAL"),
    "PROGRAM": Token(PROGRAM, "PROGRAM"),
    "PROCEDURE": Token(PROCEDURE, "PROCEDURE"),
}

#############################################
# 					Lexer					#
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

        if self.ch == "." and self.peek().isdigit():
            num += self.ch
            self.advance()
            while self.ch is not None and self.ch.isdigit():
                num += self.ch
                self.advance()
            return Token(REAL_CONST, float(num))

        return Token(INT_CONST, int(num))

    def peek(self):
        if self.pos + 1 < self.max_len:
            return self.text[self.pos + 1]
        else:
            return None

    def error(self):
        raise Exception("Lexer error.")

    def skip_comment(self):
        stack = ["{"]
        while stack:
            self.advance()
            if self.ch is not None and self.ch == "{":
                stack.append(self.ch)
            if self.ch is not None and self.ch == "}":
                stack.pop()
            if self.ch is None:
                raise Exception("Unclosed comment.")
        self.advance()

    def _id(self):
        id = ""
        if self.ch == "_":
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

        if self.ch == "+":
            self.advance()
            return Token(PLUS, "+")

        if self.ch == "-":
            self.advance()
            return Token(MINUS, "-")

        if self.ch == "*":
            self.advance()
            return Token(MUL, "*")

        if self.ch == "/":
            self.advance()
            return Token(REAL_DIV, "/")

        if self.ch == "(":
            self.advance()
            return Token(LP, "(")

        if self.ch == ")":
            self.advance()
            return Token(RP, ")")

        if self.ch == ",":
            self.advance()
            return Token(COMMA, ",")

        if self.ch == ".":
            self.advance()
            return Token(DOT, ".")

        if self.ch == ":" and self.peek() == "=":
            self.advance()
            self.advance()
            return Token(ASSIGN, ":=")

        if self.ch == ":":
            self.advance()
            return Token(COLON, ":")

        if self.ch == ";":
            self.advance()
            return Token(SEMI, ";")

        if self.ch.isalpha() or self.ch == "_":
            return self._id()

        if self.ch == "{":  # supports nexsted comments
            self.skip_comment()
            return self.get_token()


#############################################
# 					 AST					#
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


class VarDeclaration(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

    def __str__(self):
        return f"Variable (token: {self.var_node}, type: {self.type_node})"

    def __repr__(self):
        return self.__str__()


class ProcedureDeclaration(AST):
    def __init__(self, name, params, block):
        self.name = name
        self.params = params  # list of param nodes
        self.block = block


class Param(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


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
        param_nodes = []


class Assignment(AST):
    def __init__(self, var, op, expr):
        self.var = var
        self.op = op  # why is this needed?
        self.expr = expr

    def __str__(self):
        return f"Assignment(var: {self.var}, op: {self.op}, expr: {self.expr})"

    def __repr__(self):
        return self.__str__()


class UnOp(AST):
    def __init__(self, op, expr):
        self.op = op.type
        self.op_value = op.value
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
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return f"Num (value: {self.value}; type: {self.type})"

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
# 					Parser					#
#############################################


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.get_token()

    def error(self, type=None):
        raise Exception(
            f"Parser error. Expected type {type} but got Token: {self.token}"
        )

    def eat(self, type):
        if self.token.type == type:
            self.token = self.lexer.get_token()
        else:
            self.error(type)

    def program(self):
        """program : PROGRAM variable SEMI block DOT"""
        self.eat(PROGRAM)
        var = self.variable()
        program_name = var.value
        self.eat(SEMI)
        block = self.block()
        program = Program(program_name, block)

        self.eat(DOT)
        return program

    def block(self):
        """
        block : declarations compound_statement
        """
        declarations = self.declarations()
        statement = self.compound_statement()
        return Block(declarations, statement)

    def declarations(self):
        """
        declarations : VAR (variable_declaration SEMI)+
                     | (PROCEDURE ID (LP formal_parameter_list
                     RP)? SEMI block SEMI)*
                    | empry
        """
        declarations = []

        while True:
            if self.token.type == VAR:
                self.eat(VAR)
                while self.token.type == ID:
                    declarations.extend(self.variable_declaration())
                    self.eat(SEMI)

            elif self.token.type == PROCEDURE:
                self.eat(PROCEDURE)
                procedure_name = self.token.value
                self.eat(ID)
                params = []

                if self.token.type == LP:
                    self.eat(LP)
                    params = self.formal_parameter_list()
                    self.eat(RP)

                self.eat(SEMI)
                block = self.block()
                declarations.append(ProcedureDeclaration(procedure_name, params, block))
                self.eat(SEMI)

            else:
                break

        return declarations

    def variable_declaration(self):
        """
        variable_declaration : ID ((COMMA ID)* COLON
            type_spec)
        """
        variables = [Variable(self.token)]
        self.eat(ID)
        while self.token.type == COMMA:
            self.eat(COMMA)
            variables.append(Variable(self.token))
            self.eat(ID)
        self.eat(COLON)
        type = self.type_spec()
        return [VarDeclaration(variable, type) for variable in variables]

    def type_spec(self):
        """
        type_spec : INTEGER
                  | REAL
        """
        token = self.token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Type(token)
        if token.type == REAL:
            self.eat(REAL)
            return Type(token)

    def formal_parameter_list(self):
        """
        formal_parameter_list : formal_parameters
                              | formal_parameters SEMI
            formal_parameter_list
        """
        if not self.token.type == ID:
            return []

        param_list = self.formal_parameters()
        if self.token == SEMI:
            self.eat(SEMI)
            param_list.extend(self.formal_parameters())

        return param_list

    def formal_parameters(self):
        """
        formal_parameters : ID (COMMA ID)* COLON type_spec
        """
        param_tokens = [self.token]
        self.eat(ID)
        while self.token.type == COMMA:
            self.eat(COMMA)
            param_tokens.append(self.token)
            self.eat(ID)
        self.eat(COLON)
        param_type = self.type_spec()
        param_list = [Param(Variable(var), param_type) for var in param_tokens]

        return param_list

    def compound_statement(self):
        """
        compound_statement : BEGIN statement_list END
        """
        self.eat(BEGIN)
        statements = self.statement_list()
        root = Compound(statements)
        self.eat(END)
        return root

    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        statements = [self.statement()]
        while self.token.type == SEMI:
            self.eat(SEMI)
            statements.append(self.statement())
        return statements

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.token.type == ID:
            return self.assigment_statement()
        elif self.token.type == BEGIN:
            return self.compound_statement()
        else:
            return self.empty()

    def assigment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        var = self.variable()
        op = self.token
        self.eat(ASSIGN)
        expr = self.expr()
        return Assignment(var, op, expr)

    def empty(self):
        return Empty()

    def variable(self):
        """
        variable : ID
        """
        var = self.token
        self.eat(ID)
        return Variable(var)

    def factor(self):
        """
        factor : (PLUS | MINUS)factor
               | INT_CONST
               | REAL_CONST
               | LP expr RP
               | variable
        """
        token = self.token
        if token.type in (INT_CONST, REAL_CONST):
            num = Num(token.value, token.type)
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
        """
        term : factor ((MUL | INT_DIV | REAL_DIV) factor)*
        """
        node = self.factor()
        while self.token.type in (MUL, INT_DIV, REAL_DIV):
            op = self.token
            self.eat(op.type)
            right_term = self.factor()
            node = BinOp(node, op, right_term)
        return node

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
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
# 				  AST Visitors				#
#############################################


class NodeVisitor:
    def visit(self, node):
        name = "visit_" + type(node).__name__
        visitor = getattr(self, name, self.default_visitor)
        return visitor(node)

    def default_visitor(self, node):
        raise Exception(f"No method named visit_{type(node).__name__}.")


#############################################
# 				    Symbols					#
#############################################
class Symbol:
    def __init__(self, name, type_symbol=None):
        self.name = name
        self.type_symbol = type_symbol


class BuiltInTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__


class VariableSymbol(Symbol):
    def __init__(self, name, type_symbol):
        super().__init__(name, type_symbol)

    def __str__(self):
        return f"<{self.name} : {self.type_symbol}>"

    __repr__ = __str__


class ProcedureSymbol(Symbol):
    def __init__(self, name, params=None):
        super(ProcedureSymbol, self).__init__(name)
        self.params = params if params is not None else []

    def __str__(self):
        return (
            f"<{self.__class__.__name__}(name = {self.name}, params = {self.params})>"
        )

    __repr__ = __str__


#############################################
# 				  Symbol Table				#
#############################################
class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self.symbol_table = OrderedDict()
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self.initBuiltIns()

    def initBuiltIns(self):
        self.define(BuiltInTypeSymbol(INTEGER))
        self.define(BuiltInTypeSymbol(REAL))

    def define(self, symbol):
        print(f"Insert: {symbol}.")
        self.symbol_table[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        print(f"Lookup: {name}. Scope: {self.scope_name}")
        symbol = self.symbol_table.get(name)
        if symbol is not None:
            return symbol
        if current_scope_only:
            return None
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)

    def __str__(self):
        header0 = "SCOPE (SCOPED SYMBOL TABLE)"
        lines = ["\n", header0, "=" * len(header0)]
        for h_name, h_value in (
            ("Scope name: ", self.scope_name),
            ("Scope level: ", self.scope_level),
            (
                "Enclosing scope:",
                (self.enclosing_scope.scope_name if self.enclosing_scope else None),
            ),
        ):
            lines.append(f"{h_name}{h_value}")
        header1 = "Scoped symbol table contents:"
        lines += ["-" * len(header1), header1]
        lines.extend(
            ("%7s: %r" % (key, value)) for key, value in self.symbol_table.items()
        )
        lines.append("\n")
        s = "\n".join(lines)
        return s

    __repr__ = __str__


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scope = None

    def visit_Program(self, program):
        print("ENTER scope: global")
        global_scope = ScopedSymbolTable(
            scope_name="global", scope_level=1, enclosing_scope=self.current_scope
        )
        self.current_scope = global_scope

        self.visit(program.block)

        print(global_scope)
        self.current_scope = self.current_scope.enclosing_scope
        print("exit scope: global")

    def visit_Block(self, block):
        for declaration in block.declarations:
            self.visit(declaration)
        self.visit(block.compound_statement)

    def visit_ProcedureDeclaration(self, procedure):
        procedure_name = procedure.name
        procedure_symbol = ProcedureSymbol(procedure_name)
        self.current_scope.define(procedure_symbol)

        print(f"ENTER scope: {procedure_name}")
        procedure_scope = ScopedSymbolTable(
            scope_name=procedure_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope,
        )

        self.current_scope = procedure_scope

        for param in procedure.params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VariableSymbol(param_name, param_type)
            self.current_scope.define(var_symbol)
            procedure_symbol.params.append(var_symbol)

        self.visit(procedure.block)

        print(procedure_scope)
        self.current_scope = self.current_scope.enclosing_scope

        print(f"EXIT scope: {procedure_name}")

    def visit_Compound(self, compound):
        for statement in compound.statement_list:
            self.visit(statement)

    def visit_Assignment(self, assignment):
        self.visit(assignment.var)
        self.visit(assignment.expr)

    def visit_Variable(self, variable):
        var_name = variable.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(variable))
        # return var_symbol.type_symbol

    def visit_VarDeclaration(self, declaration):
        var_name = declaration.var_node.value
        type_name = declaration.type_node.value  # string containing type name
        type_symbol = self.current_scope.lookup(type_name)
        if self.current_scope.lookup(var_name, current_scope_only=True) is not None:
            raise Exception(f"Variable {var_name} declared twice in the same scope.")
        var_symbol = VariableSymbol(var_name, type_symbol)
        self.current_scope.define(var_symbol)

    def visit_Type(self, type):
        pass

    def visit_UnOp(self, unop):
        return self.visit(unop.expr)

    def visit_BinOp(self, binop):
        left = self.visit(binop.left)
        right = self.visit(binop.right)
        if left == right:
            return left
        else:
            raise Exception(
                f"Type error: applying {binop.op} to a {left} and a {right}"
            )

    def visit_Num(self, num):
        type = num.type
        if type == INT_CONST:
            return INTEGER
        if type == REAL_CONST:
            return REAL

    def visit_Empty(self, empty):
        pass


#############################################
# 				  Interpreter				#
#############################################


class Interpreter(NodeVisitor):
    GLOBAL_MEMORY = {}

    def __init__(self, tree):
        self.tree = tree

    def interpret(self):
        if self.tree is None:
            return ""
        return self.visit(self.tree)

    def visit_Program(self, program):
        return self.visit(program.block)

    def visit_Block(self, block):
        for declaration in block.declarations:
            self.visit(declaration)

        return self.visit(block.compound_statement)

    def visit_VarDeclaration(self, declaration):
        pass

    def visit_ProcedureDeclaration(self, procedure):
        pass

    def visit_Type(self, type_node):
        pass

    def visit_Compound(self, compound):
        for statement in compound.statement_list:
            self.visit(statement)

    def visit_Assignment(self, assignment):
        var_name = assignment.var.value
        self.GLOBAL_MEMORY[var_name] = self.visit(assignment.expr)

    def visit_Variable(self, var_node):
        var_name = var_node.value
        val = self.GLOBAL_MEMORY.get(var_name)
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
        if op == REAL_DIV:
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


#############################################
# 				  	Main					#
#############################################


def main():
    import sys

    print("=" * 41)
    print("Welcome to your Simple Pascal Interpreter")
    print("=" * 41)

    text = open(
        "/Users/paultalma/Programming/simple-interpreters/pascal-interpreter/test.txt",
        "r",
    ).read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symbol_table_builder = SemanticAnalyzer()
    symbol_table_builder.visit_Program(tree)

    interpreter = Interpreter(tree)
    result = interpreter.interpret()


if __name__ == "__main__":
    main()
