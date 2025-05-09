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
                    fs.append(Return(Integer(Type('int'),0)))
                newprog.append(Function(n, p, fs))
            case _:
                newprog.append(s)
    return Program(newprog)


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":

    assert add_returns(Program([Function(Name(TEST_TYPE,"f"), [Name(TEST_TYPE,"x")], [Print(Name(TEST_TYPE,"x"))])])) == Program(
        [
            Function(
                name=Name(TEST_TYPE,str="f"),
                params=[Name(TEST_TYPE,str="x")],
                statements=[Print(value=Name(TEST_TYPE,str="x")), Return(value=Integer(Type("int"),n=0))],
            )
        ]
    )

    prog = Program(
        [
            Function(
                Name(TEST_TYPE,"f"),
                [Name(TEST_TYPE,"y")],
                [
                    IfElse(
                        Relation(TEST_TYPE,RelationOp("=="), Name(TEST_TYPE,"y"), Integer(TEST_TYPE,5)),
                        [Return(Name(TEST_TYPE,"y"))],
                        [Print(Name(TEST_TYPE,"y"))],
                    ),
                ],
            ),
            Function(
                Name(TEST_TYPE,"g"),
                [Name(TEST_TYPE,"y")],
                [Return(Name(TEST_TYPE,"y"))],
            ),
            IfElse(
                Relation(TEST_TYPE,RelationOp("=="), Name(TEST_TYPE,"y"), Integer(TEST_TYPE,5)),
                [Print(Name(TEST_TYPE,"y"))],
                [],
            ),
            Print(Name(TEST_TYPE,"x")),
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
                    name=Name(TEST_TYPE,str="f"),
                    params=[Name(TEST_TYPE,str="y")],
                    statements=[
                        IfElse(
                            condition=Relation(TEST_TYPE,op=RelationOp(name="=="), left=Name(TEST_TYPE,str="y"), right=Integer(TEST_TYPE,n=5)),
                            iflist=[Return(value=Name(TEST_TYPE,str="y"))],
                            elselist=[Print(value=Name(TEST_TYPE,str="y"))],
                        ),
                        Return(value=Integer(Type("int"),n=0)),
                    ],
                ),
                Function(name=Name(TEST_TYPE,str="g"), params=[Name(TEST_TYPE,str="y")], statements=[Return(value=Name(TEST_TYPE,str="y"))]),
                IfElse(
                    condition=Relation(TEST_TYPE,op=RelationOp(name="=="), left=Name(TEST_TYPE,str="y"), right=Integer(TEST_TYPE,n=5)),
                    iflist=[Print(value=Name(TEST_TYPE,str="y"))],
                    elselist=[],
                ),
                Print(value=Name(TEST_TYPE,str="x")),
            ]
        ),
    )
    printcolor("tests PASSED", ansicode.green)
