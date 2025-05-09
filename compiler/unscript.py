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
        newprog.append(Function(Name(Type("int"),"mainuser"), [Name(Type("int"),"argc"), Name(TEST_TYPE,"arg1"), Name(TEST_TYPE,"arg2")], main))
    else: 
        newprog.append(Function(Name(Type("int"),"main"), [], main))
    return Program(newprog)


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    ast = Program(
        [
            Declare(Name(TEST_TYPE,"x")),
            Assign(Name(TEST_TYPE,"x"), Integer(TEST_TYPE,42)),
            Function(
                Name(TEST_TYPE,"f"),
                [Name(TEST_TYPE,"y")],
                [Declare(Name(TEST_TYPE,"t")), Assign(Name(TEST_TYPE,"t"), Multiply(TEST_TYPE, Name(TEST_TYPE,"x"), Name(TEST_TYPE,"y"))), Return(Name(TEST_TYPE,"t"))],
            ),
            IfElse(
                Relation(TEST_TYPE, RelationOp("=="), Name(TEST_TYPE,"x"), Integer(TEST_TYPE,5)),
                [
                    Declare(Name(TEST_TYPE,"x")),
                    Assign(Name(TEST_TYPE,"x"), Integer(TEST_TYPE,13)),
                ],
                [Print(Name(TEST_TYPE,"x"))],
            ),
            Print(Name(TEST_TYPE,"x")),
        ]
    )
    #    print(format_program(ast))
    ast = resolve_scopes(ast)
    prog = unscript_toplevel(ast)
    #    print(prog)
    #    printcolor(format_program(prog))

    assert prog == Program(
        [
            GlobalVar(Name(TEST_TYPE,"x")),
            Function(
                Name(TEST_TYPE,"f"),
                [Name(TEST_TYPE,"y")],
                [
                    LocalVar(Name(TEST_TYPE,"t")),
                    Assign(LocalName(TEST_TYPE,"t"), Multiply(TEST_TYPE, GlobalName(TEST_TYPE,"x"), LocalName(TEST_TYPE,"y"))),
                    Return(LocalName(TEST_TYPE,"t")),
                ],
            ),
            Function(
                Name(Type("int"),"main"),
                [],
                [
                    Assign(GlobalName(TEST_TYPE,"x"), Integer(TEST_TYPE,42)),
                    IfElse(
                        Relation(TEST_TYPE,RelationOp("=="), GlobalName(TEST_TYPE,"x"), Integer(TEST_TYPE,5)),
                        [LocalVar(Name(TEST_TYPE,"x")), Assign(LocalName(TEST_TYPE,"x"), Integer(TEST_TYPE,13))],
                        [Print(GlobalName(TEST_TYPE,"x"))],
                    ),
                    Print(GlobalName(TEST_TYPE,"x")),
                ],
            ),
        ]
    )

    printcolor("minimal tests (also test resolve_scope) PASSED", ansicode.green)
