# simple-interpreters

Working up to implementing an interpreter for a simple language. `calc.py` is an interpreter for a simple calculator.

Thanks to [Ruslan Spivak](https://ruslanspivak.com).

## TODOs

### Calculator

-   [x] handle multi-digit input
-   [x] handle subtraction
-   [x] handle whitespace around parts of input
-   [x] multiplication
-   [x] division
    -   [x] div by 0
-   [x] arbitrary length add/subtract
-   [x] mul/div and plus/minus
-   [x] parentheses
-   [x] AST
    -   [ ] C++ implementation for ASTs (hard—no polymorphism and no introspection!)
-   [x] separate parser and interpreter
-   [x] unary operators

### Simple Pascal Interpreter

-   [x] add new token types
-   [x] write lexer
-   [x] write parser
-   [x] write interpreter
-   [ ] variable types
    -   [ ] type checking
-   [x] replace '/' with 'div'
-   [x] make keywords and identifiers case insensitive
-   [x] variable names can start with '\_'
-   [ ] comments
