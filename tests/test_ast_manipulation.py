"""Early and somewhat out of date version of tests for the first ~5 stags of the compiler
(all AST manipulation steps, nothing about tokenizing or parsing), as a separate program I can 
easily run. However, more recently have moved unit tests into individual modules."""
# TODO:
# [ ] decide whether to keep or delete this

# Add compiler/ sibling directory to sys.path so we can import the modules we want to test
#  (not necessarily best practice for project structure but this is a quick standalone test)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../compiler")))

from model import *
from format import *
from deinit import *
from foldconstants import *
from resolve_scope import *
from unscript import *
from defaultreturns import *
from manual_test import *

print("Testing foldconstants...")

tests = (
    {
        "in": Program(
            [
                Print(Add(Multiply(Integer(2), Integer(3)), Name("x"))),
                Print(Multiply(Add(Integer(1), Multiply(Integer(2), Integer(3))), Integer(4))),
            ]
        ),
        "out": Program([Print(Add(Integer(6), Name("x"))), Print(Integer(28))]),
    },
    {
        "in": Program(
            [
                Function(
                    Name("miscmath"),
                    [Name("a"), Name("b")],
                    [
                        IfElse(
                            Relation(RelationOp("<"), Name("a"), Add(Integer(5), Integer(3))),
                            [
                                DeclareValue(Name("x"), Multiply(Integer(2), Integer(3))),
                                Return(Multiply(Add(Integer(3), Integer(4)), Name("a"))),
                            ],
                            [Return(Integer(4))],
                        )
                    ],
                ),
                DeclareValue(Name("x"), Integer(3)),
                Print(CallFn(Name("miscmath"), [Add(Integer(2), Add(Integer(2), Integer(7))), Name("x")])),
            ],
        ),
        "out": Program(
            [
                Function(
                    Name("miscmath"),
                    [Name("a"), Name("b")],
                    [
                        IfElse(
                            Relation(RelationOp("<"), Name("a"), Integer(8)),
                            [
                                DeclareValue(Name("x"), Integer(6)),
                                Return(Multiply(Integer(7), Name("a"))),
                            ],
                            [Return(Integer(4))],
                        )
                    ],
                ),
                DeclareValue(Name("x"), Integer(3)),
                Print(CallFn(Name("miscmath"), [Integer(11), Name("x")])),
            ]
        ),
    },
)

for test in tests:
    assert fold_constants(test["in"]) == test["out"]

printcolor("PASSED", ansicode.green)

tests = (
    {
        "in": Program(
            [
                Function(
                    Name("foo"),
                    [Name("a"), Name("b")],
                    [
                        DeclareValue(Name("x"), Add(Integer(2), Integer(3))),
                        IfElse(
                            Relation(RelationOp("<"), Name("x"), Add(Integer(5), Integer(3))),
                            [DeclareValue(Name("z"), Integer(8)), Return(Name("z"))],
                            [Return(Integer(5))],
                        ),
                    ],
                ),
            ]
        ),
        "out": Program(
            [
                Function(
                    Name("foo"),
                    [Name("a"), Name("b")],
                    [
                        Declare(Name("x")),
                        Assign(Name("x"), Add(Integer(2), Integer(3))),
                        IfElse(
                            Relation(RelationOp("<"), Name("x"), Add(Integer(5), Integer(3))),
                            [Declare(Name("z")), Assign(Name("z"), Integer(8)), Return(Name("z"))],
                            [Return(Integer(5))],
                        ),
                    ],
                ),
            ]
        ),
    },
)

print("Testing deinit...")
for test in tests:
    assert deinit_variables(test["in"]) == test["out"]
printcolor("PASSED", ansicode.green)

print("Testing resolve...")
tests = (
    {
        "in": Program(
            [
                Declare(Name("x")),
                Assign(Name("x"), Integer(42)),
                Function(
                    Name("f"),
                    [Name("y")],
                    [Declare(Name("t")), Assign(Name("t"), Multiply(Name("x"), Name("y"))), Return(Name("t"))],
                ),
                Function(
                    Name("g"),
                    [Name("x")],
                    [Return(Name("x"))],
                ),
                # CHECK: The 'x' in h(z) should be global x, as the local x from g(x) was for that function only...
                Function(
                    Name("h"),
                    [Name("z")],
                    [Return(Name("x"))],
                ),
                IfElse(
                    Relation(RelationOp("=="), Name("x"), Integer(5)),
                    [  # CHECK: this x should be local because it's declared inside an If
                        Declare(Name("x")),
                        Assign(Name("x"), Integer(13)),
                        Print(CallFn(Name("f"), [Name("x")])),
                    ],
                    [
                        # CHECK: this x should be global again since x is not declared locally in the else
                        Print(Name("x"))
                    ],
                ),
                # CHECK: this x should be global
                Print(Name("x")),
            ]
        ),
        "out": Program(
            [
                GlobalVar(Name("x")),
                Assign(GlobalName("x"), Integer(42)),
                Function(
                    Name("f"),
                    [Name("y")],
                    [LocalVar(Name("t")), Assign(LocalName("t"), Multiply(GlobalName("x"),LocalName("y"))), Return(LocalName("t"))],
                ),
                Function(
                    Name("g"),
                    [Name("x")],
                    [Return(LocalName("x"))],
                ),
                # CHECK: The 'x' in h(z) should be global x, as the local x from g(x) was for that function only...
                Function(
                    Name("h"),
                    [Name("z")],
                    [Return(GlobalName("x"))],
                ),
                IfElse(
                    Relation(RelationOp("=="), GlobalName("x"), Integer(5)),
                    [  # CHECK: this x should be local because it's declared inside an If
                        LocalVar(Name("x")),
                        Assign(LocalName("x"), Integer(13)),
                        Print(CallFn(Name("f"), [LocalName("x")])),
                    ],
                    [
                        # CHECK: this x should be global again since x is not declared locally in the else
                        Print(GlobalName("x"))
                    ],
                ),
                # CHECK: this x should be global
                Print(GlobalName("x")),
            ]
        ),
    },
)
for test in tests:
    #print(resolve_scopes(test["in"]))
    #printcolor(str(test["out"]))
    assert(resolve_scopes(test["in"]) == test["out"])
    
printcolor("PASSED", ansicode.green)

print("Testing defaultreturns...")
tests = (
    {
        "in": Program(
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
                # CHECK: this x should be global
                Print(Name("x")),
            ]
        ),
        "out": Program(
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
                        Return(Integer(0)),
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
                # CHECK: this x should be global
                Print(Name("x")),
            ]
        ),
    },
)
for test in tests:
    assert add_returns(test["in"]) == test["out"]
printcolor("PASSED", ansicode.green)

print("Testing unscript...")
tests = (
    {
        "in": Program(
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
        ),
        "out": Program(
            [
                Declare(Name("x")),
                Function(
                    Name("f"),
                    [Name("y")],
                    [Declare(Name("t")), Assign(Name("t"), Multiply(Name("x"), Name("y"))), Return(Name("t"))],
                ),
                Function(
                    Name("main"),
                    [],
                    [
                        Assign(Name("x"), Integer(42)),
                        IfElse(
                            Relation(RelationOp("=="), Name("x"), Integer(5)),
                            [
                                Declare(Name("x")),
                                Assign(Name("x"), Integer(13)),
                            ],
                            [Print(Name("x"))],
                        ),
                        Print(Name("x")),
                    ],
                ),
            ]
        ),
    },
)
for test in tests:
    assert unscript_toplevel(test["in"]) == test["out"]
    pass
printcolor("PASSED", ansicode.green)

print("Integration tests running compile()...")

tests = (
    {
        "in": Program(
            [
                Function(
                    Name("add1"),
                    [Name("x")],
                    [Assign(Name("x"), Add(Name("x"), Integer(1)))],
                ),
                DeclareValue(Name("x"), Integer(10)),
                Print(Add(Multiply(Integer(2), Integer(3)), CallFn(Name("add1"), [Name("x")]))),
                Print(Name("x")),
            ]
        ),
        "out": Program(
            [
                Function(
                    Name("add1"),
                    [Name("x")],
                    [Assign(LocalName("x"), Add(LocalName("x"), Integer(1))), Return(Integer(0))],
                ),
                GlobalVar(Name("x")),
                Function(
                    Name("main"),
                    [],
                    [
                        Assign(GlobalName("x"), Integer(10)),
                        Print(Add(Integer(6), CallFn(Name("add1"), [GlobalName("x")]))),
                        Print(GlobalName("x")),
                        Return(Integer(0)),
                    ],
                ),
            ]
        ),
    },
)

for test in tests:
    # print(test["in"])
    prog = compile(test["in"])
    # printcolor(str(prog))
    # printcolor(str(test["out"]),ansicode.yellow)
    assert prog == test["out"]

printcolor("PASSED", ansicode.green)

# Program(statements=[Function(name=Name(str='add1'), params=[Name(str='x')], statements=[Assign(left=LocalName(str='x'),
#  right=Add(left=LocalName(str='x'), right=Integer(n=1))), Return(value=Integer(n=0))]), GlobalVar(name=Name(str='x')),
#  Function(name=Name(str='main'), params=[], statements=[Assign(left=GlobalName(str='x'), right=Integer(n=10)),
#  Print(value=Add(left=Integer(n=6), right=CallFn(name=Name(str='add1'), params=[GlobalName(str='x')]))), Print(value=GlobalName(str='x')),
#  Return(value=Integer(n=0))])])
# Program(statements=[Function(name=Name(str='add1'), params=[Name(str='x')], statements=[Assign(left=LocalName(str='x'),
#  right=Add(left=LocalName(str='x'), right=Integer(n=1))), Return(value=Integer(n=0))]), GlobalVar(name=Name(str='x')),
#  Function(name=Name(str='main'), params=[], statements=[Assign(left=GlobalName(str='x'), right=Integer(n=10)),
#  Print(value=Add(left=Integer(n=6), right=CallFn(name=Name(str='add1'), params=[GlobalName(str='x')]))), Print(value=GlobalName(str='x'))])])
