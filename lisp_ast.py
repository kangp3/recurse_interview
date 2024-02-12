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


if __name__ == "__main__":
    src = "(first (list 1 (+ 2 3) 9))"
    assert lisp_ast(src) == ["first", ["list", 1, ["+", 2, 3], 9]]
    assert lisp_ast("(+ 2 3)") == ["+", 2, 3]
    assert lisp_ast("(+ a b)") == ["+", 'a', 'b']

    pprint_result(src)
    pprint_result("(+ 2 3)")
