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
                    fs.append(Return(Integer(DUMMYTYPE,0)))
                newprog.append(Function(n, p, fs))
            case _:
                newprog.append(s)
    return Program(newprog)


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":

    assert add_returns(Program([Function(Name(DUMMYTYPE,"f"), [Name(DUMMYTYPE,"x")], [Print(Name(DUMMYTYPE,"x"))])])) == Program(
        [
            Function(
                name=Name(DUMMYTYPE,str="f"),
                params=[Name(DUMMYTYPE,str="x")],
                statements=[Print(value=Name(DUMMYTYPE,str="x")), Return(value=Integer(DUMMYTYPE,n=0))],
            )
        ]
    )

    prog = Program(
        [
            Function(
                Name(DUMMYTYPE,"f"),
                [Name(DUMMYTYPE,"y")],
                [
                    IfElse(
                        Relation(DUMMYTYPE,RelationOp("=="), Name(DUMMYTYPE,"y"), Integer(DUMMYTYPE,5)),
                        [Return(Name(DUMMYTYPE,"y"))],
                        [Print(Name(DUMMYTYPE,"y"))],
                    ),
                ],
            ),
            Function(
                Name(DUMMYTYPE,"g"),
                [Name(DUMMYTYPE,"y")],
                [Return(Name(DUMMYTYPE,"y"))],
            ),
            IfElse(
                Relation(DUMMYTYPE,RelationOp("=="), Name(DUMMYTYPE,"y"), Integer(DUMMYTYPE,5)),
                [Print(Name(DUMMYTYPE,"y"))],
                [],
            ),
            Print(Name(DUMMYTYPE,"x")),
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
                    name=Name(DUMMYTYPE,str="f"),
                    params=[Name(DUMMYTYPE,str="y")],
                    statements=[
                        IfElse(
                            condition=Relation(DUMMYTYPE,op=RelationOp(name="=="), left=Name(DUMMYTYPE,str="y"), right=Integer(DUMMYTYPE,n=5)),
                            iflist=[Return(value=Name(DUMMYTYPE,str="y"))],
                            elselist=[Print(value=Name(DUMMYTYPE,str="y"))],
                        ),
                        Return(value=Integer(DUMMYTYPE,n=0)),
                    ],
                ),
                Function(name=Name(DUMMYTYPE,str="g"), params=[Name(DUMMYTYPE,str="y")], statements=[Return(value=Name(DUMMYTYPE,str="y"))]),
                IfElse(
                    condition=Relation(DUMMYTYPE,op=RelationOp(name="=="), left=Name(DUMMYTYPE,str="y"), right=Integer(DUMMYTYPE,n=5)),
                    iflist=[Print(value=Name(DUMMYTYPE,str="y"))],
                    elselist=[],
                ),
                Print(value=Name(DUMMYTYPE,str="x")),
            ]
        ),
    )
    printcolor("tests PASSED", ansicode.green)
