"""Simple compiler pass that moves all top-level statements other than global variable declaration 
into a main() function.

This allows later compiler steps to treat the top-level program as a mix of only global variable
definition and function definitions and treat the contents of the "main" function in the same way
as any other function.

Previous compiler stage: resolve.py
Next compiler stage: defaultreturns.py"""

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
       WIP: If argmode==true, instead wrap in mainuser() and assume we'll link the output with a
        helper function in C with a main() that passes command-line arguments to mainuser()."""
    newprog = []
    main = []

    for s in prog.statements:
        match s:
            case Declare() | DeclareValue() | Function():
                newprog.append(s)
            case _:
                main.append(s)

    if argmode:
        # Assumes this will be linked to a wrapper that passes argc and arg1 to this user code function
        # The following resolve_scope compiler pass will see argc and arg1 being used in user code,
        #   match them to the mainuser(argc,arg1) function signature, and scope them as local variables
        newprog.append(Function(Name("mainuser"), [Name("argc"), Name("arg1")], main))
    else: 
        newprog.append(Function(Name("main"), [], main))
    return Program(newprog)


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    ast = Program(
        [
            Declare(Name("x")),
            Assign(Name("x"), Integer(42)),
            Function(
                Name("f"),
                [Name("y")],
                [Declare(Name("t")), Assign(Name("t"), Multiply(Name("x"), Name("y"))), Return(Name("t"))],
            ),
            IfElse(
                Relation(RelationOp("=="), Name("x"), Integer(5)),
                [
                    Declare(Name("x")),
                    Assign(Name("x"), Integer(13)),
                ],
                [Print(Name("x"))],
            ),
            Print(Name("x")),
        ]
    )
    #    print(format_program(ast))
    ast = resolve_scopes(ast)
    prog = unscript_toplevel(ast)
    #    print(prog)
    #    printcolor(format_program(prog))

    assert prog == Program(
        [
            GlobalVar(Name("x")),
            Function(
                Name("f"),
                [Name("y")],
                [
                    LocalVar(Name("t")),
                    Assign(LocalName("t"), Multiply(GlobalName("x"), LocalName("y"))),
                    Return(LocalName("t")),
                ],
            ),
            Function(
                Name("main"),
                [],
                [
                    Assign(GlobalName("x"), Integer(42)),
                    IfElse(
                        Relation(RelationOp("=="), GlobalName("x"), Integer(5)),
                        [LocalVar(Name("x")), Assign(LocalName("x"), Integer(13))],
                        [Print(GlobalName("x"))],
                    ),
                    Print(GlobalName("x")),
                ],
            ),
        ]
    )

    printcolor("minimal tests (also test resolve_scope) PASSED", ansicode.green)
