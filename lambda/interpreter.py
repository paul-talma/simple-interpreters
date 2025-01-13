from main.terms import Abstraction


class NodeVisitor:
    def visit(self, node):
        name = "visit_" + type(node).__name__
        visitor = getattr(self, name, self.default_visitor)
        return visitor(node)

    def default_visitor(self, node):
        raise Exception(f"No method named visit_{type(node).__name__}.")


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree

    def interpret(self):
        if self.tree is None:
            return ""
        return self.visit(self.tree)

    def visit_Variable(self, variable):
        return variable

    def visit_Abstraction(self, abstraction):
        var = self.visit(abstraction.var)
        expr = self.visit(abstraction.expr)
        res = Abstraction(var, expr)
        return res

    def visit_Application(self, application):
        func = application.func
        if type(func) is Abstraction:
            var = func.var
            expr = func.expr
            arg = application.arg
            res = expr.substitute(var, arg)
            res = self.visit(res)
            return res
        return application
