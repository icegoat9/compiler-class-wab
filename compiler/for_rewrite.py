# for_rewrite.py
"""Replaces all For structures in the AST with equivalent While structures.

Run this early after parsing, as later compiler passes don't understand For structures.

This iteratively / recursively descends into If / Elif / Else / While structures as these
structures may be nested within each other.

Previous compiler stage: elif_rewrite.py
Next compiler stage: fold_constants.py
"""

# TODO
# [X] decide whether this or elif_rewrite.py will run first (probably elif_rewrite)
#     (whichever one runs first needs to understand the structures of the other to
#      descend into it recursively, but not vice-versa)
# [X] modify elif_rewrite.py to handle For structures
# [ ] test in case of pre-existing loop variable declaration
# [X] assertion-based unit tests
#   [ ] more complex nested For and nested withing (function, if, while, etc)
# [ ] call as a compiler pass in the top-level compile_ast

from model import *
from format import *


def for_program(program: Program) -> Program:
    """Process program, rewrite for to while, return new program."""
    return Program(for_statements(program.statements))


def for_statements(statements: list[Statement]) -> list[Statement]:
    """Process a list of statements, rewriting for to while.

    Run on the main program, but also called recurively while processing the bodies of control flow structures.
    """
    slist = []
    # TODO: some better way to replace for loop with a list comprehension?
    for s in statements:
        # extend = append each statement from list elif_statments() one by one
        slist.extend(for_statement(s))
    return slist


def for_statement(s: Statement) -> list[Statement]:
    """Process single statement, return list of processed statements (possibly just containing one item).

    If a For object is found, rewrite it as a While object.

    Also process the statement bodies of (While, If, Function) to look for For objects within them.
    """
    match s:
        case IfElse(relation, iflist, elselist):
            return [IfElse(relation, for_statements(iflist), for_statements(elselist))]
        case While(relation, iflist):
            return [While(relation, for_statements(iflist))]
        case Function(name, params, body):
            return [Function(name, params, for_statements(body))]
        case For(init, condition, increment, body):
            # init = Assign(name, value)
            # condition = Relation(op, left, right)
            # increment = Assign(name, value)
            return [
                DeclareValue(init.left, init.right),
                While(
                    condition,
                    for_statements(body) + [increment],
                )
            ]
        case _:
            return [s]


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    prog = Program(
        [
            For(
                Assign(Name("i"), Integer(1)),
                Relation(RelationOp("<"), Name("i"), Integer(2)),
                Assign(Name("i"), Add(Name("i"),Integer(1))),
                [Print(Name("i"))]
            ),
        ]
    )
    # print("Input program: %s\n" % prog)
    print(format_program(prog))
    out = for_program(prog)
    # print("Output program: %s\n" % out)
    print("IS REWRITTEN AS:\n")
    print(format_program(out))
    assert out == Program(
        [
            DeclareValue(Name("i"), Integer(1)),
            While(Relation(RelationOp("<"), Name("i"), Integer(2)),
                  [Print(Name("i")),
                   Assign(Name("i"), Add(Name("i"), Integer(1)))])
        ]
    )
    printcolor("tests PASSED", ansicode.green)
