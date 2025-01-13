# these classes define the nodes in the AST


class Term:
    def __repr__(self) -> str:
        pass

    def substitute(self, term1, term2):
        pass


class Variable(Term):
    def __init__(self, name: int):
        self.name = name

    def substitute(self, x: Term, term: Term) -> Term:
        return term if self.name == x.name else self

    def __repr__(self) -> str:
        return f"x_{self.name}"


class Abstraction(Term):
    def __init__(self, var: Variable, expr: Term):
        self.var = var
        self.expr = expr

    def substitute(self, x: Variable, term: Term) -> Term:
        # x is bound
        if x.name == self.var.name:
            return self

        # x is in FV(self) and var is in FV(term)
        # need to find a fresh variable and substitute to avoid clash
        self_fvs = free_variables(self)
        term_fvs = free_variables(term)
        if x in self_fvs and self.var in term_fvs:
            fvs = self_fvs.union(term_fvs)
            z = find_fresh_fv(fvs)
            sub_z_for_x = self.substitute(self.var, z)
            sub_term_for_x = sub_z_for_x.substitute(x, term)
            res = Abstraction(z, sub_term_for_x)
            return res

        # x is not free in self, or var is not free in term
        sub_term_for_x = self.expr.substitute(x, term)
        res = Abstraction(self.var, sub_term_for_x)
        return res

    def __repr__(self) -> str:
        return f"(λ{self.var} . {self.expr})"


class Application(Term):
    def __init__(self, function: Term, argument: Term):
        self.func = function
        self.arg = argument

    def substitute(self, x: Variable, term: Term):
        new_func = self.func.substitute(x, term)
        new_arg = self.arg.substitute(x, term)
        res = Application(new_func, new_arg)
        return res

    def __repr__(self) -> str:
        return f"({self.func} {self.arg})"


def free_variables(term: Term) -> set[Variable]:
    """
    recursively compute the free variables of expr
    """
    if type(term) is Variable:
        return {term}

    if type(term) is Abstraction:
        var = term.var
        expr = term.expr
        free_vars = free_variables(expr)
        if var in free_vars:
            free_vars.remove(var)

        return free_vars

    # term is application
    func = term.func
    arg = term.arg
    func_vars = free_variables(func)
    arg_vars = free_variables(arg)
    return func_vars.union(arg_vars)


def find_fresh_fv(vars: set[Variable]) -> Variable:
    """
    return the variable with lowest index not in vars
    """
    length = vars.size()
    indices = [var.name for var in vars]
    for i in range(length + 1):
        if i not in indices:
            return Variable(i)
