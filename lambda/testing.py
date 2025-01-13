from parser import ParserError
from run import parse, interpret, transpile


def get_input(path):
    with open(path, "r") as file:
        lines = file.readlines()

    return lines


def process(line):
    try:
        tree = parse(line)
    except ParserError as e:
        print(f"Unable to parse line: {line}. Error: {str(e)}")
    else:
        tree_latex = transpile(tree)
        try:
            normal_form = interpret(tree)
        except RecursionError:
            print("This expression doesn't have a normal form!")
        else:
            normal_form_latex = transpile(normal_form)
            print(f"Original expression: {tree_latex}.")
            print(f"Normal form: {normal_form_latex}.")


def process_input(input):
    for id, line in enumerate(input):
        print("================")
        print(f"Processing input line {id + 1}")
        process(line)


if __name__ == "__main__":
    path = "test_expressions.txt"
    input = get_input(path)
    process_input(input)
