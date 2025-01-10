# resolve.py
"""Resolve variable scope across entire program AST: replace each variable definition or use with an
explicit Global or Local classification (by subtituting in new Local and Global subclasses for objects).

Previous compiler stage: deinit.py
Next compiler stage: unscript.py"""

#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests (note: minimal)


# TODOs:
# [X] rename more descriptively?
# [ ] make tougher unit tests with nested ifs, or if in a function
# [X] combine islocal and localvars into a data structure / class?
# [X]    more involved class with add_to_scope and child_scope methods vs just copying?
# [X] catch some undefined variables error?

from model import *
from format import *


def resolve_scopes(program: Program) -> Program:
    """Resolve all variable scopes in program."""
    return Program(resolve_scope_statements(program.statements))


def resolve_scope_statements(statements: list[Statement], scope: Scope = Scope()) -> list[Statement]:
    """Resolve all variable scopes in a list of statements (whether top-level program or the
    list of statements within some flow control structure such as If/While)."""
    return [resolve_scope_statement(s, scope) for s in statements]


def resolve_scope_statement(s: Statement, scope: Scope) -> Statement:
    """Resolve all variable scopes in this statement (including recursively on contained statement blocks
    if relevenat). For example, the generic Declare class becomes GlobalVar or LocalVar."""
    # print("DEBUG: "+str(s))
    match s:
        case Print(x):
            return Print(resolve_scope_expr(x, scope))
        case Assign(x, y):
            return Assign(resolve_scope_expr(x, scope), resolve_scope_expr(y, scope))
        case Declare(x):
            scope.declare(x)
            if scope.isglobalscope():
                return GlobalVar(x)
            else:
                return LocalVar(x)
        case IfElse(relation, iflist, elselist):
            return IfElse(
                resolve_scope_expr(relation, scope),
                resolve_scope_statements(iflist, scope.new_child_scope()),
                resolve_scope_statements(elselist, scope.new_child_scope()),
            )
        case While(relation, s):
            return While(
                resolve_scope_expr(relation, scope),
                resolve_scope_statements(s, scope.new_child_scope()),
            )
        case Return(x):
            return Return(resolve_scope_expr(x, scope))
        case Function(n, params, s):
            # Create a new child scope for the function and add passed parameters to it
            fscope = scope.new_child_scope()
            for p in params:
                fscope.declare(p)
            return Function(n, params, resolve_scope_statements(s, fscope))
        case _:
            raise RuntimeError(f"Unhandled case {s}")


def resolve_scope_expr(e: Expression, scope: Scope) -> Expression:
    """Resolve all variable scopes in this expression (and child expressions). e.g. Name -> LocalName or GlobalName."""
    # print("DEBUG %s, localvars %s" % (e, localvars))
    match e:
        case Name(x):
            if scope.getscope(x) == "local":
                return LocalName(x)
            elif scope.getscope(x) == "global":
                return GlobalName(x)
            else:
                raise RuntimeError("Name %s referenced before definition" % x)
        case Add(x, y):
            return Add(
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Multiply(x, y):
            return Multiply(
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Subtract(x, y):
            return Subtract(
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Divide(x, y):
            return Divide(
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case CallFn(name, params):
            # resolve scope of any variable passed as parameter
            return CallFn(name, [resolve_scope_expr(p, scope) for p in params])
        case Relation(op, left, right):
            return Relation(op, resolve_scope_expr(left, scope), resolve_scope_expr(right, scope))
        case Integer() | RelationOp():
            return e
        case _:
            raise RuntimeError(f"Unhandled resolve_scope Expression {e}")


# prog = Program([While(Relation(RelationOp("<"), Name("x"), Integer(5)),[Return(Integer(5))])])
# print(prog)
# print(format_program(resolve_scopes(prog)))
# quit()

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
    )
    # print(ast)
    #    print(format_program(ast))
    #    print("-- resolve_scopes() test --")
    #    print(resolve_scopes(ast))
    #    printcolor(format_program(resolve_scopes(ast)))

    assert resolve_scopes(ast) == Program(
        [
            GlobalVar(Name("x")),
            Assign(GlobalName("x"), Integer(42)),
            Function(
                Name("f"),
                [Name("y")],
                [
                    LocalVar(Name("t")),
                    Assign(LocalName("t"), Multiply(GlobalName("x"), LocalName("y"))),
                    Return(LocalName("t")),
                ],
            ),
            Function(Name("g"), [Name("x")], statements=[Return(LocalName("x"))]),
            Function(Name("h"), [Name("z")], statements=[Return(GlobalName("x"))]),
            IfElse(
                Relation(RelationOp("=="), GlobalName("x"), Integer(5)),
                [
                    LocalVar(Name("x")),
                    Assign(LocalName("x"), Integer(13)),
                    Print(CallFn(Name("f"), [LocalName("x")])),
                ],
                [Print(GlobalName("x"))],
            ),
            Print(GlobalName("x")),
        ]
    )

    # Now intentionally throw an undefined variable error
    ast = Program(
        [
            Function(
                Name("f"),
                [Name("y")],
                [Declare(Name("t")), Assign(Name("t"), Multiply(Name("x"), Name("y"))), Return(Name("t"))],
            ),
            Print(Name("t")),
        ]
    )
    #    print("----\n%s" % format_program(ast))
    #    print("-- resolve_scopes() test, should give undefined variable error --")
    # print(resolve_scopes(ast))
    try:
        format_program(resolve_scopes(ast))
    except RuntimeError as err:
        #        printcolor(str(err), ansicode.yellow)
        assert str(err) == "Name t referenced before definition"

    printcolor("minimal tests PASSED", ansicode.green)
