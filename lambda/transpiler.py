from main.interpreter import NodeVisitor


class LatexTranspiler(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree

    def transpile(self):
        if self.tree is None:
            return ""

        latex_expression = self.visit(self.tree)
        return latex_expression

    def visit_Variable(self, variable):
        latex_var = "x_{" + str(variable.name) + "}"
        return latex_var

    def visit_Abstraction(self, abstraction):
        latex_abs = "\\lambda "

        latex_var = self.visit(abstraction.var)
        latex_expr = self.visit(abstraction.expr)

        latex_abs += latex_var + "." + latex_expr

        return latex_abs

    def visit_Application(self, application):
        latex_app = "("

        latex_func = self.visit(application.func)
        latex_arg = self.visit(application.arg)

        latex_app += latex_func + latex_arg + ")"

        return latex_app
