# defaultreturns.py
"""Add default 'return 0' statement to the end of all function definitions.

This makes end of function flow control explicit for later transformation into assembly code."""
#
# Cleanup TODO
# [X] docstrings
# [X] assertion-based unit tests

from model import *
from format import *
from debughelper import *


def add_returns(prog: Program) -> Program:
    """Add 'return 0' to all function definitions in program."""
    newprog = []
    in_function = False
    for s in prog.statements:
        match s:
            case Function(n, p, fs):
                # If function doesn't end with a Return, add Return 0
                if not isinstance(fs[-1], Return):
                    fs.append(Return(Integer(0)))
                newprog.append(Function(n, p, fs))
            case _:
                newprog.append(s)
    return Program(newprog)


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":

    assert add_returns(Program([Function(Name("f"), [Name("x")], [Print(Name("x"))])])) == Program(
        [
            Function(
                name=Name(str="f"),
                params=[Name(str="x")],
                statements=[Print(value=Name(str="x")), Return(value=Integer(n=0))],
            )
        ]
    )

    prog = Program(
        [
            Function(
                Name("f"),
                [Name("y")],
                [
                    IfElse(
                        Relation(RelationOp("=="), Name("y"), Integer(5)),
                        [Return(Name("y"))],
                        [Print(Name("y"))],
                    ),
                ],
            ),
            Function(
                Name("g"),
                [Name("y")],
                [Return(Name("y"))],
            ),
            IfElse(
                Relation(RelationOp("=="), Name("y"), Integer(5)),
                [Print(Name("y"))],
                [],
            ),
            Print(Name("x")),
        ]
    )
    #    print(format_program(prog))
    #    printcolor(format_program(add_returns(prog)))
    prog2 = add_returns(prog)
    #    print(prog2)
    assert_equal_verbose(
        prog2,
        Program(
            statements=[
                Function(
                    name=Name(str="f"),
                    params=[Name(str="y")],
                    statements=[
                        IfElse(
                            condition=Relation(op=RelationOp(name="=="), left=Name(str="y"), right=Integer(n=5)),
                            iflist=[Return(value=Name(str="y"))],
                            elselist=[Print(value=Name(str="y"))],
                        ),
                        Return(value=Integer(n=0)),
                    ],
                ),
                Function(name=Name(str="g"), params=[Name(str="y")], statements=[Return(value=Name(str="y"))]),
                IfElse(
                    condition=Relation(op=RelationOp(name="=="), left=Name(str="y"), right=Integer(n=5)),
                    iflist=[Print(value=Name(str="y"))],
                    elselist=[],
                ),
                Print(value=Name(str="x")),
            ]
        ),
    )
    printcolor("tests PASSED", ansicode.green)
