# manual_test.py
"""Scratchpad, somewhat out of date, for calling and testing various compiler modules in combination,
to manually explore output and test issues. See compile.py and test_compile_roundtrip.py for more recent
work on this topic."""

# Add compiler/ sibling directory to sys.path so we can import the modules we want to test
#  (not necessarily best practice for project structure but this is a quick standalone test)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../compiler")))

from model import *
from format import *
import deinit
import foldconstants
import resolve_scope
import unscript
import defaultreturns

# TODO / notes to self (see also TODO.md and individual files):
# [X] Anywhere a bare string (e.g. "<", "x") is being passed, decide if that should be a class
# [X]    e.g. Name("x") or RelationOp(RelationOp("<"))
# [X] Think through where parentheses get applied
# [ ] Remove redundancy with compile.py (import below from that?)

# Apply all the compiling / rewriting we've done so far
def compile(program: Program, debug: bool = False) -> Program:
    if debug:
        print("--original---\n%s" % format_program(program))
    program = foldconstants.fold_constants(program)
    if debug:
        print("--foldconstants---\n%s" % format_program(program))
    program = deinit.deinit_variables(program)
    if debug:
        print("--deinit---\n%s" % format_program(program))
    program = resolve_scope.resolve_scopes(program)
    if debug:
        print("--resolve---\n%s" % format_program(program))
    program = unscript.unscript_toplevel(program)
    if debug:
        print("--unscript---\n%s" % format_program(program))
    program = defaultreturns.add_returns(program)
    if debug:
        print("--defaultreturns---\n%s" % format_program(program))
    return program


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":

    core_programs = [
        [
            DeclareValue(Name("x"), Integer(10)),
            Assign(Name("x"), Add(Name("x"), Integer(1))),
            Print(Add(Multiply(Integer(23), Integer(45)), Name("x"))),
        ],
        [
            DeclareValue(Name("x"), Integer(3)),
            DeclareValue(Name("y"), Integer(4)),
            DeclareValue(Name("min"), Integer(0)),
            IfElse(
                Relation(RelationOp("<"), Name("x"), Name("y")),
                [Assign(Name("min"), Name("x"))],
                [Assign(Name("min"), Name("y"))],
            ),
            Print(Name("min")),
        ],
        [
            DeclareValue(Name("result"), Integer(1)),
            DeclareValue(Name("x"), Integer(1)),
            While(
                Relation(RelationOp("<"), Name("x"), Integer(10)),
                [
                    Assign(Name("result"), Multiply(Name("result"), Name("x"))),
                    Assign(Name("x"), Add(Name("x"), Integer(1))),
                ],
            ),
            Print(Name("result")),
        ],
        [
            Function(
                Name("add1"),
                [Name("x")],
                [Assign(Name("x"), Add(Name("x"), Integer(1))), Return(Name("x"))],
            ),
            DeclareValue(Name("x"), Integer(10)),
            Print(Add(Multiply(Integer(23), Integer(45)), CallFn(Name("add1"), [Name("x")]))),
            Print(Name("x")),
        ],
    ]

    other_programs = [
        [
            Function(
                Name("fact"),
                [Name("n")],
                [
                    DeclareValue(Name("result"), Integer(1)),
                    DeclareValue(Name("x"), Integer(1)),
                    While(
                        Relation(RelationOp("<"), Name("x"), Name("n")),
                        [
                            Assign(Name("result"), Multiply(Name("result"), Name("x"))),
                            Assign(Name("x"), Add(Name("x"), Integer(1))),
                        ],
                    ),
                    Return(Multiply(Name("result"), Name("n"))),
                ],
            ),
            DeclareValue(Name("n"), Integer(0)),
            While(
                Relation(RelationOp("<"), Name("n"), Integer(10)),
                [
                    Print(CallFn(Name("fact"), [Name("n")])),
                    Assign(Name("n"), Add(Name("n"), Integer(1))),
                ],
            ),
        ],
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
        [
            Function(
                Name("miscmath"),
                [Name("a"), Name("b")],
                [
                    IfElse(
                        Relation(RelationOp("<"), Name("a"), Add(Integer(5), Integer(3))),
                        [
                            Return(
                                Multiply(
                                    Add(Integer(3), Integer(4)),
                                    Add(Name("a"), Multiply(Name("a"), Name("b"))),
                                )
                            )
                        ],
                        [Return(Integer(4))],
                    )
                ],
            ),
            DeclareValue(Name("x"), CallFn(Name("miscmath"), [Add(Integer(2), Add(Integer(2), Integer(7))), Integer(13)])),
        ],
    ]

    for i, statements in enumerate(core_programs):
        program = Program(statements)
        print("--- WAB Program #%d ---" % (i + 1))
        # print("INPUT:\n" + str(program))
        # Print a formatted version of the program
        print(format_program(program))
        print("-- Compiled: --")
        printcolor(format_program(compile(program)))

    # quit()

    for i, statements in enumerate(other_programs):
        program = Program(statements)
        print("--- Other More Complex Test Program #%d ---" % (i + 1))
        # print("INPUT:\n" + str(program))
        # Print a formatted version of the program
        print(format_program(program))
        print("-- Compiled: --")
        printcolor(format_program(compile(program)), ansicode.lightblue)

    # show step by step

    compile(Program(core_programs[-1]), debug=True)
