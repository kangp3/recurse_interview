def lisp_ast_toks(toks):
    ast = []
    assert toks, "No tokens found"

    first_tok = toks.pop(0)
    # Assume source code always contains an operator
    # Can be modified to accept a single literal as well
    assert first_tok == "(", "Non-functional first token"

    while toks:
        if toks[0] == "(":
            # Recursively parse sub-ASTs on a nested open paren
            sub_ast, toks = lisp_ast_toks(toks)
            ast.append(sub_ast)
            continue

        tok = toks.pop(0)
        if tok == ')':
            # Run until a closing paren indicates end of args
            return ast, toks

        # Attempt to cast as an int and return as-is otherwise
        try:
            cast_tok = int(tok)
        except ValueError:
            cast_tok = tok

        ast.append(cast_tok)

    assert False, "Mismatched parens"


def lisp_ast(src):
    # Add whitespace around parens to make tokenizing a bit cleaner
    # NOTE: This plays poorly with string-literals that contain parens
    src = src.replace('(', '( ')
    src = src.replace(')', ' )')
    toks = src.split()

    # Grab the first returned element since the second is the consumed remainder of tokens
    return lisp_ast_toks(toks)[0]


def pprint_result(src):
    print(src, '\n  ->', lisp_ast(src))


def evaluate_statement(ast):
    op = ast[0]
    args = ast[1:]

    casted_args = []
    for arg in args:
        if type(arg) == list:
            casted_args.append(evaluate_statement(arg))
        else:
            casted_args.append(arg)

    return evaluate_op(op, casted_args)


def evaluate_op(op, args):
    if op == "+":
        return sum(args)
    if op == "list":
        return list(args)
    if op == "first":
        assert len(args) == 1
        return args[0][0]
    if op == "logand":
        assert len(args) == 2
        return args[0] & args[1]


if __name__ == "__main__":
    src = "(first (list 1 (+ 2 3) 9))"
    assert lisp_ast(src) == ["first", ["list", 1, ["+", 2, 3], 9]]
    assert lisp_ast("(+ 2 3)") == ["+", 2, 3]
    assert lisp_ast("(+ a b)") == ["+", 'a', 'b']

    # pprint_result(src)
    # pprint_result("(+ 2 3)")

    print(evaluate_statement(["+", 2, 3]))
    print(evaluate_statement(["+", 1, ["+", 2, 3], 4]))  # 1 + (2 + 3) + 4
    print(evaluate_statement(["list", 1, ["+", 2, 3], 9]))  # 1, 5, 9
    print(evaluate_statement(["first", ["list", 1, ["+", 2, 3], 9]]))  # 1
    print(evaluate_statement(["logand", 2, 3]))  # 10 & 11 -> 10
    print(evaluate_statement(["+", 1, ["logand", 2, 3], 4]))  # 1 + 2 + 4 -> 7
