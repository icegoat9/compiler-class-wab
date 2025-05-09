"""Simple compiler pass that moves all top-level statements other than global variable declaration 
into a main() function.

This allows later compiler steps to treat the top-level program as a mix of only global variable
definition and function definitions and treat the contents of the "main" function in the same way
as any other function.

Previous compiler stage: deinit.py
Next compiler stage: resolve.py"""

#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests (one minimal, should better localize to this module)

from model import *
from format import *
from resolve_scope import *

def unscript_toplevel(prog: Program, argmode: bool=False) -> Program:
    """Wrap all user code except variable and function declartions in a main() function.
       If argmode==true, instead wrap in mainuser() and assume we'll link the output with a
        helper function in C with a main() that passes up to two command-line arguments to mainuser()."""
    newprog = []
    main = []

    for s in prog.statements:
        match s:
            case Declare() | DeclareValue() | Function() | StrConstNum():
                newprog.append(s)
            case _:
                main.append(s)

    if argmode:
        # Assumes this will be linked to a wrapper that passes argc,arg1,arg2 to this user code function
        # The following resolve_scope compiler pass will see those arg variables being used in user code,
        #   match them to the mainuser(argc,arg1,arg2) function signature, and scope them as local variables
        newprog.append(Function(Name(DUMMYTYPE,"mainuser"), [Name(DUMMYTYPE,"argc"), Name(DUMMYTYPE,"arg1"), Name(DUMMYTYPE,"arg2")], main))
    else: 
        newprog.append(Function(Name(DUMMYTYPE,"main"), [], main))
    return Program(newprog)


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    ast = Program(
        [
            Declare(Name(DUMMYTYPE,"x")),
            Assign(Name(DUMMYTYPE,"x"), Integer(DUMMYTYPE,42)),
            Function(
                Name(DUMMYTYPE,"f"),
                [Name(DUMMYTYPE,"y")],
                [Declare(Name(DUMMYTYPE,"t")), Assign(Name(DUMMYTYPE,"t"), Multiply(DUMMYTYPE, Name(DUMMYTYPE,"x"), Name(DUMMYTYPE,"y"))), Return(Name(DUMMYTYPE,"t"))],
            ),
            IfElse(
                Relation(DUMMYTYPE, RelationOp("=="), Name(DUMMYTYPE,"x"), Integer(DUMMYTYPE,5)),
                [
                    Declare(Name(DUMMYTYPE,"x")),
                    Assign(Name(DUMMYTYPE,"x"), Integer(DUMMYTYPE,13)),
                ],
                [Print(Name(DUMMYTYPE,"x"))],
            ),
            Print(Name(DUMMYTYPE,"x")),
        ]
    )
    #    print(format_program(ast))
    ast = resolve_scopes(ast)
    prog = unscript_toplevel(ast)
    #    print(prog)
    #    printcolor(format_program(prog))

    assert prog == Program(
        [
            GlobalVar(Name(DUMMYTYPE,"x")),
            Function(
                Name(DUMMYTYPE,"f"),
                [Name(DUMMYTYPE,"y")],
                [
                    LocalVar(Name(DUMMYTYPE,"t")),
                    Assign(LocalName(DUMMYTYPE,"t"), Multiply(DUMMYTYPE, GlobalName(DUMMYTYPE,"x"), LocalName(DUMMYTYPE,"y"))),
                    Return(LocalName(DUMMYTYPE,"t")),
                ],
            ),
            Function(
                Name(DUMMYTYPE,"main"),
                [],
                [
                    Assign(GlobalName(DUMMYTYPE,"x"), Integer(DUMMYTYPE,42)),
                    IfElse(
                        Relation(DUMMYTYPE,RelationOp("=="), GlobalName(DUMMYTYPE,"x"), Integer(DUMMYTYPE,5)),
                        [LocalVar(Name(DUMMYTYPE,"x")), Assign(LocalName(DUMMYTYPE,"x"), Integer(DUMMYTYPE,13))],
                        [Print(GlobalName(DUMMYTYPE,"x"))],
                    ),
                    Print(GlobalName(DUMMYTYPE,"x")),
                ],
            ),
        ]
    )

    printcolor("minimal tests (also test resolve_scope) PASSED", ansicode.green)
