# deinit.py
"""Split 'var x = 10' definitions in AST into separate 'declare var x' and 'x = 10' statements.

This small compiler pass makes variable definition explicit and standalone, to slightly simplify
a later compiler pass that resolves variable scope and variable definitions and local or global.

Previous compiler stage: foldconstants.py
Next compiler stage: resolve.py"""
#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests
# [ ] Replace for loop, see below

from model import *
from format import *
from debughelper import *


def deinit_variables(program: Program) -> Program:
    """Run deinit process on entire program."""
    return Program(deinit_statements(program.statements))


def deinit_statements(statements: list[Statement]) -> list[Statement]:
    """Deinit a list of statements, could be at the top program level, or a list of statements
    nested within a Function, IfElse, While, or so on."""
    slist = []
    # TODO: some better way to replace for loop with a list comprehension?
    for s in statements:
        # print("DEBUG " + str(deinit_statement(s)))
        # extend = append each statement from list deinit_statments() one by one
        slist.extend(deinit_statement(s))
    return slist


def deinit_statement(s: Statement) -> list[Statement]:
    """Deinit a statement, returning a list of output statements (for simple statements, this will
    be a list of one item, but for flow control structures like IfElse, this runs deinit on their
    contents, potentially recursively).
    """
    match s:
        case DeclareValue(name, expr):
            return [Declare(name), Assign(name, expr)]
        case IfElse(relation, iflist, elselist):
            return [IfElse(relation, deinit_statements(iflist), deinit_statements(elselist))]
        case While(relation, s):
            return [While(relation, deinit_statements(s))]
        case Function(n, p, s):
            return [Function(n, p, deinit_statements(s))]
        case Print() | Assign() | Return():
            # Listed all these remaining cases out so we can save the fallthrough case _ for errors
            return [s]
        case _:
            raise RuntimeError(f"Unhandled deinit_statement() case {s}")


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    #    print("A few deinit.py test cases:")
    test_program_statements = [
        [DeclareValue(Name("z"), Integer(3))],
        [
            Function(
                Name("foo"),
                [Name("a"), Name("b")],
                [
                    DeclareValue(Name("x"), Add(Integer(2), Integer(3))),
                    DeclareValue(Name("y"), Add(Name("a"), Integer(4))),
                    IfElse(
                        Relation(RelationOp("<"), Name("x"), Add(Integer(5), Integer(3))),
                        [DeclareValue(Name("z"), Integer(8)), Return(Name("z"))],
                        [Return(Integer(5))],
                    ),
                ],
            ),
            DeclareValue(Name("z"), Integer(3)),
        ],
    ]
    for s in test_program_statements:
        #        print("-- program to be folded: --")
        p = Program(s)
    #        print(format_program(p))
    #        print("-- after folding: --")
    #        print(format_program(deinit_variables(p)))
    #        print(deinit_variables(p))

    assert deinit_variables(Program([DeclareValue(Name("z"), Integer(3))])) == Program(
        [Declare(Name("z")), Assign(Name("z"), Integer(3))]
    )
    assert deinit_variables(
        Program(
            [
                Function(
                    Name("foo"),
                    [Name("a"), Name("b")],
                    [
                        DeclareValue(Name("x"), Add(Integer(2), Integer(3))),
                        DeclareValue(Name("y"), Add(Name("a"), Integer(4))),
                        IfElse(
                            Relation(RelationOp("<"), Name("x"), Add(Integer(5), Integer(3))),
                            [DeclareValue(Name("z"), Integer(8)), Return(Name("z"))],
                            [Return(Integer(5))],
                        ),
                    ],
                ),
                DeclareValue(Name("z"), Integer(3)),
            ]
        )
    ) == Program(
        [
            Function(
                Name("foo"),
                [Name("a"), Name("b")],
                [
                    Declare(Name("x")),
                    Assign(Name("x"), Add(Integer(2), Integer(3))),
                    Declare(Name("y")),
                    Assign(Name("y"), Add(Name("a"), Integer(4))),
                    IfElse(
                        Relation(RelationOp("<"), Name("x"), Add(Integer(5), Integer(3))),
                        [
                            Declare(Name("z")),
                            Assign(Name("z"), Integer(8)),
                            Return(Name("z")),
                        ],
                        [Return(Integer(5))],
                    ),
                ],
            ),
            Declare(Name("z")),
            Assign(Name("z"), Integer(3)),
        ]
    )

    printcolor("tests PASSED", ansicode.green)
